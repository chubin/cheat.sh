;;; cheat-sh.el --- Interact with cheat.sh  -*- lexical-binding: t -*-
;; Copyright 2017 by Dave Pearson <davep@davep.org>

;; Author: Dave Pearson <davep@davep.org>
;; Version: 1.7
;; Keywords: docs, help
;; URL: https://github.com/davep/cheat-sh.el
;; Package-Requires: ((emacs "24"))

;; cheat-sh.el is free software distributed under the terms of the GNU
;; General Public Licence, version 2 or (at your option) any later version.
;; For details see the file COPYING.

;;; Commentary:
;;
;; cheat-sh.el provides a simple Emacs interface for looking things up on
;; cheat.sh.

;;; Code:

(require 'url-vars)

(defgroup cheat-sh nil
  "Interact with cheat.sh."
  :group 'docs)

(defface cheat-sh-section
  '((t :inherit (bold font-lock-doc-face)))
  "Face used on sections in a cheat-sh output window."
  :group 'cheat-sh)

(defface cheat-sh-caption
  '((t :inherit (bold font-lock-function-name-face)))
  "Face used on captions in the cheat-sh output window."
  :group 'cheat-sh)

(defcustom cheat-sh-list-timeout (* 60 60 4)
  "Seconds to wait before deciding the cached sheet list is \"stale\"."
  :type 'integer
  :group 'cheat-sh)

(defconst cheat-sh-url "http://cheat.sh/%s?T"
  "URL for cheat.sh.")

(defconst cheat-sh-user-agent "cheat-sh.el (curl)"
  "User agent to send to cheat.sh.

Note that \"curl\" should ideally be included in the user agent
string because of the way cheat.sh works.

cheat.sh looks for a specific set of clients in the user
agent (see https://goo.gl/8gh95X for this) to decide if it should
deliver plain text rather than HTML. cheat-sh.el requires plain
text.")

(defun cheat-sh-get (thing)
  "Get THING from cheat.sh."
  (let* ((url-request-extra-headers `(("User-Agent" . ,cheat-sh-user-agent)))
         (buffer (url-retrieve-synchronously (format cheat-sh-url (url-hexify-string thing)) t t)))
    (when buffer
      (with-current-buffer buffer
        (setf (point) (point-min))
        (when (search-forward-regexp "^$" nil t)
          (buffer-substring (point) (point-max)))))))

(defvar cheat-sh-sheet-list nil
  "List of all available sheets.")

(defvar cheat-sh-sheet-list-acquired nil
  "The time when variable `cheat-sh-sheet-list' was populated.")

(defun cheat-sh-sheet-list-cache ()
  "Return the list of sheets.

The list is cached in memory, and is considered \"stale\" and is
refreshed after `cheat-sh-list-timeout' seconds."
  (when (and cheat-sh-sheet-list-acquired
             (> (- (time-to-seconds) cheat-sh-sheet-list-acquired) cheat-sh-list-timeout))
    (setq cheat-sh-sheet-list nil))
  (or cheat-sh-sheet-list
      (let ((list (cheat-sh-get ":list")))
        (when list
          (setq cheat-sh-sheet-list-acquired (time-to-seconds))
          (setq cheat-sh-sheet-list (split-string list "\n"))))))

(defun cheat-sh-read (prompt)
  "Read input from the user, showing PROMPT to prompt them.

This function is used by some `interactive' functions in
cheat-sh.el to get the item to look up. It provides completion
based of the sheets that are available on cheat.sh."
  (completing-read prompt (cheat-sh-sheet-list-cache)))

(defun cheat-sh-decorate-all (buffer regexp face)
  "Decorate BUFFER, finding REGEXP and setting face to FACE."
  (with-current-buffer buffer
    (save-excursion
      (setf (point) (point-min))
      (while (search-forward-regexp regexp nil t)
        (replace-match (propertize (match-string 1) 'font-lock-face face) nil t)))))

(defun cheat-sh-decorate-results (buffer)
  "Decorate BUFFER with properties to highlight results."
  ;; "[Search section]"
  (cheat-sh-decorate-all buffer "^\\(\\[.*\\]\\)$"        'cheat-sh-section)
  ;; "# Result caption"
  (cheat-sh-decorate-all buffer "^\\(#.*\\)$"             'cheat-sh-caption)
  ;; "cheat-sh help caption:"
  (cheat-sh-decorate-all buffer "^\\([^[:space:]].*:\\)$" 'cheat-sh-caption))

;;;###autoload
(defun cheat-sh (thing)
  "Look up THING on cheat.sh and display the result."
  (interactive (list (cheat-sh-read "Lookup: ")))
  (let ((result (cheat-sh-get thing)))
    (if result
        (with-help-window "*cheat.sh*"
          (princ result)
          (cheat-sh-decorate-results standard-output))
      (error "Can't find anything for %s on cheat.sh" thing))))

;;;###autoload
(defun cheat-sh-region (start end)
  "Look up the text between START and END on cheat.sh."
  (interactive "r")
  (deactivate-mark)
  (cheat-sh (buffer-substring-no-properties start end)))

;;;###autoload
(defun cheat-sh-maybe-region ()
  "If region is active lookup content of region, otherwise prompt."
  (interactive)
  (call-interactively (if mark-active #'cheat-sh-region #'cheat-sh)))

;;;###autoload
(defun cheat-sh-help ()
  "Get help on using cheat.sh."
  (interactive)
  (cheat-sh ":help"))

;;;###autoload
(defun cheat-sh-list (thing)
  "Get a list of topics available on cheat.sh.

Either gets a topic list for subject THING, or simply gets a list
of all available topics on cheat.sh if THING is supplied as an
empty string."
  (interactive (list (cheat-sh-read "List sheets for: ")))
  (cheat-sh (format "%s/:list" thing)))

;;;###autoload
(defun cheat-sh-search (thing)
  "Search for THING on cheat.sh and display the result."
  (interactive "sSearch: ")
  (cheat-sh (concat "~" thing)))

;;;###autoload
(defun cheat-sh-search-topic (topic thing)
  "Search TOPIC for THING on cheat.sh and display the result."
  (interactive
   (list (cheat-sh-read "Topic: ")
         (read-string "Search: ")))
  (cheat-sh (concat topic "/~" thing)))

(provide 'cheat-sh)

;;; cheat-sh.el ends here
