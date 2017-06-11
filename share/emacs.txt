;;; cheat-sh.el --- Interact with cheat.sh  -*- lexical-binding: t -*-
;; Copyright 2017 by Dave Pearson <davep@davep.org>

;; Author: Dave Pearson <davep@davep.org>
;; Version: 1.3
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
  (with-current-buffer
      (let ((url-request-extra-headers `(("User-Agent" . ,cheat-sh-user-agent))))
        (url-retrieve-synchronously (format cheat-sh-url (url-hexify-string thing)) t t))
    (setf (point) (point-min))
    (when (search-forward-regexp "^$" nil t)
      (buffer-substring (point) (point-max)))))

(defvar cheat-sh-sheet-list nil
  "List of all available sheets.")

(defun cheat-sh-read (prompt)
  "Read input from the user, showing PROMPT to prompt them.

This function is used by some `interactive' functions in
cheat-sh.el to get the item to look up. It provides completion
based of the sheets that are available on cheat.sh."
  (completing-read prompt
                   (or cheat-sh-sheet-list
                       (setq cheat-sh-sheet-list (split-string (cheat-sh-get ":list") "\n")))))

;;;###autoload
(defun cheat-sh (thing)
  "Look up THING on cheat.sh and display the result."
  (interactive (list (cheat-sh-read "Lookup: ")))
  (let ((result (cheat-sh-get thing)))
    (if result
        (with-help-window "*cheat.sh*"
          (princ result))
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
