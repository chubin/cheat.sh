describe("Awesomplete.$", function () {

	$.fixture("options");

	subject(function () { return Awesomplete.$(this.expression, this.context) });

	describe("with default context", itFindsElement);

	describe("with custom context", function () {
		def("context", function () { return fixture.el });

		itFindsElement();
	});

	describe("with truthy non string expression", function () {
		it("returns the expression back", function () {
			this.expression = $("#no-options");
			expect(this.subject).toBe(this.expression);
		});
	});

	describe("with falsy non string expression", function () {
		it("returns null if expression is undefined", function () {
			this.expression = undefined;
			expect(this.subject).toBeNull();
		});

		it("returns null if expression is null", function () {
			this.expression = null;
			expect(this.subject).toBeNull();
		});

		it("returns null if expression is false", function () {
			this.expression = false;
			expect(this.subject).toBeNull();
		});
	});

	// Shared behaviors

	function itFindsElement() {
		it("returns DOM element", function () {
			this.expression = "#no-options";
			expect(this.subject instanceof HTMLElement).toBe(true);
		});

		it("finds by id", function () {
			this.expression = "#no-options";
			expect(this.subject.id).toEqual("no-options");
		});

		it("finds by class name", function () {
			this.expression = ".simple-input";
			expect(this.subject.id).toEqual("no-options");
		});

		it("finds by tag name", function () {
			this.expression = "datalist";
			expect(this.subject.id).toEqual("list");
		});
	}
});
