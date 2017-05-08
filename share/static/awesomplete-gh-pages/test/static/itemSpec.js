describe("Awesomplete.ITEM", function () {

	subject(function () { return Awesomplete.ITEM });

	def("element", function () { return this.subject("JavaScript", this.input || "") });

	it("creates DOM element", function () {
		expect(this.element instanceof HTMLElement).toBe(true);
	});

	it("creates LI element", function () {
		expect(this.element.tagName).toBe("LI");
	});

	it("sets aria-selected to false", function () {
		expect(this.element.getAttribute("aria-selected")).toBe("false");
	});

	describe("with matched input", function () {
		def("input", "jav");

		it("marks the match", function () {
			expect(this.element.innerHTML).toBe("<mark>Jav</mark>aScript");
		});
	});

	describe("with multiple matches", function () {
		def("input", "a");

		it("marks all matches", function () {
			expect(this.element.innerHTML).toBe("J<mark>a</mark>v<mark>a</mark>Script");
		});
	});

	describe("with no match", function () {
		def("input", "foo");

		it("does not mark anything", function () {
			expect(this.element.innerHTML).toBe("JavaScript");
		});
	});

	describe("with empty input", function () {
		def("input", "");

		it("does not mark anything", function () {
			expect(this.element.innerHTML).toBe("JavaScript");
		});
	});

	describe("with space input", function () {
		def("input", " ");

		it("does not mark anything", function () {
			expect(this.element.innerHTML).toBe("JavaScript");
		});
	});
});
