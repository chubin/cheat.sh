describe("Awesomplete.$$", function () {

	$.fixture("options");

	subject(function () { return Awesomplete.$$(this.expression, this.context) });

	describe("with default context", itFindsAllElements);

	describe("with custom context", function () {
		def("context", function () { return fixture.el });

		itFindsAllElements();
	});

	// Shared behaviors

	function itFindsAllElements() {
		it("returns an array of DOM elements", function () {
			this.expression = "#no-options";
			expect(this.subject).toEqual(jasmine.any(Array));
			expect(this.subject[0] instanceof HTMLElement).toBe(true);
		});

		it("finds all elements", function () {
			this.expression = "input";
			expect(this.subject.length).toEqual($$("input").length);
		});

		it("finds DOM element", function () {
			this.expression = "#no-options";
			expect(this.subject[0] instanceof HTMLElement).toBe(true);
		});

		it("finds by id", function () {
			this.expression = "#no-options";
			expect(this.subject[0].id).toEqual("no-options");
		});

		it("finds by class name", function () {
			this.expression = ".simple-input";
			expect(this.subject[0].id).toEqual("no-options");
		});

		it("finds by tag name", function () {
			this.expression = "datalist";
			expect(this.subject[0].id).toEqual("list");
		});
	}
});
