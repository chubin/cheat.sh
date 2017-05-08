describe("Awesomplete.FILTER_CONTAINS", function () {

	subject(function () { return Awesomplete.FILTER_CONTAINS });

	describe("search in a plain string", function () {
		it("matches at the start", function () {
			expect(this.subject("Hello world", "Hello")).toBe(true);
		});

		it("matches in the middle", function () {
			expect(this.subject("Ticket to the moon", "to the")).toBe(true);
		});

		it("matches at the end", function () {
			expect(this.subject("This is the end", "end")).toBe(true);
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

		it("matches in the middle", function () {
			expect(this.subject("[^j(a)v?a-sc|ri\\p+t*]{.$}", "sc|ri\\p+t*")).toBe(true);
		});

		it("matches at the end", function () {
			expect(this.subject("[^j(a)v?a-sc|ri\\p+t*]{.$}", "{.$}")).toBe(true);
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
