describe("Awesomplete.FILTER_STARTSWITH", function () {

	subject(function () { return Awesomplete.FILTER_STARTSWITH });

	describe("search in plain string", function () {
		it("matches at the start", function () {
			expect(this.subject("Hello world", "Hello")).toBe(true);
		});

		it("does not match in the middle", function () {
			expect(this.subject("Ticket to the moon", "to the")).toBe(false);
		});

		it("does not match at the end", function () {
			expect(this.subject("This is the end", "end")).toBe(false);
		});

		it("performs case insensitive match", function () {
			expect(this.subject("Hey You", "HEY YOU")).toBe(true);
		});

		it("ignores whitespaces around the search value", function () {
			expect(this.subject("Watch this", "  Watch  ")).toBe(true);
		});

		it("does not match if substring is not found", function () {
			expect(this.subject("No", "way")).toBe(false);
		});
	});

	describe("search in string with special RegExp chars", function () {
		it("matches at the start", function () {
			expect(this.subject("[^j(a)v?a-sc|ri\\p+t*]{.$}", "[^j(a)v?a-")).toBe(true);
		});

		it("does not match in the middle", function () {
			expect(this.subject("[^j(a)v?a-sc|ri\\p+t*]{.$}", "sc|ri\\p+t*")).toBe(false);
		});

		it("does not match at the end", function () {
			expect(this.subject("[^j(a)v?a-sc|ri\\p+t*]{.$}", "{.$}")).toBe(false);
		});

		it("performs case insensitive match", function () {
			expect(this.subject("[^j(a)v?a-sc|ri\\p+t*]{.$}", "[^J(A)V?A-SC|RI\\P+T*]{.$}")).toBe(true);
		});

		it("ignores whitespaces around the search value", function () {
			expect(this.subject("[^j(a)v?a-sc|ri\\p+t*]{.$}", "  [^j(a)v?a-  ")).toBe(true);
		});

		it("does not match if substring is not found", function () {
			expect(this.subject("[^j(a)v?a-sc|ri\\p+t*]{.$}", "no way")).toBe(false);
		});
	});
});
