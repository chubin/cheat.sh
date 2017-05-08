describe("Awesomplete.SORT_BYLENGTH", function () {

	subject(function () { return Awesomplete.SORT_BYLENGTH });

	describe("with strings of different length", function () {
		it("returns negative number if the first string is shorter", function () {
			expect(this.subject("a", "aa")).toBe(-1);
			expect(this.subject("a", "bb")).toBe(-1);
			expect(this.subject("b", "aa")).toBe(-1);

			expect(this.subject("a", "aaa")).toBe(-2);
			expect(this.subject("a", "bbb")).toBe(-2);
			expect(this.subject("b", "aaa")).toBe(-2);
		});

		it("returns positive number if the first string is longer", function () {
			expect(this.subject("aa", "a")).toBe(1);
			expect(this.subject("bb", "a")).toBe(1);
			expect(this.subject("aa", "b")).toBe(1);

			expect(this.subject("aaa", "a")).toBe(2);
			expect(this.subject("bbb", "a")).toBe(2);
			expect(this.subject("aaa", "b")).toBe(2);
		});
	});

	describe("with strings of the same length", function () {
		it("returns -1 if the first string < second string", function () {
			expect(this.subject("a", "b")).toBe(-1);
			expect(this.subject("aa", "bb")).toBe(-1);
			expect(this.subject("aaa", "bbb")).toBe(-1);
		});

		it("returns 1 if the first string > second string", function () {
			expect(this.subject("b", "a")).toBe(1);
			expect(this.subject("bb", "aa")).toBe(1);
			expect(this.subject("bbb", "aaa")).toBe(1);
		});

		// FIXME SORT_BYLENGTH should probably return 0 like classic string comparison
		it("returns 1 if the first string == second string", function () {
			expect(this.subject("a", "a")).toBe(1);
			expect(this.subject("aa", "aa")).toBe(1);
			expect(this.subject("aaa", "aaa")).toBe(1);
		});
	});
});
