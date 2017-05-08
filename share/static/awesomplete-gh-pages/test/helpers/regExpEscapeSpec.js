describe("Awesomplete.$.regExpEscape", function () {

	subject(function () { return Awesomplete.$.regExpEscape(this.str) });

	describe("with regular expression special characters", function () {
		it("escapes backslashes", function () {
			this.str = "\\";
			expect(this.subject).toBe("\\\\");
		});

		it("escapes brackets, braces and parentheses", function () {
			this.str = "[]{}()";
			expect(this.subject).toBe("\\[\\]\\{\\}\\(\\)");
		});

		it("escapes other special characters", function () {
			this.str = "-^$*+?.|";
			expect(this.subject).toBe("\\-\\^\\$\\*\\+\\?\\.\\|");
		});

		it("escapes the whole string", function () {
			this.str = "**";
			expect(this.subject).toBe("\\*\\*");
		});
	});

	describe("with plain characters", function () {
		it("does not escape letters", function () {
			this.str = "abcdefjhijklmnopqrstuvwxyzABCDEFJHIJKLMNOPQRSTUVWXYZ";
			expect(this.subject).toBe(this.str);
		});

		it("does not escape numbers", function () {
			this.str = "0123456789";
			expect(this.subject).toBe(this.str);
		});
	});
});
