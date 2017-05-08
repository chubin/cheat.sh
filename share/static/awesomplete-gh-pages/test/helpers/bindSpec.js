describe("Awesomplete.$.bind", function () {

	$.fixture("plain");

	subject(function () {
		return function () { Awesomplete.$.bind(this.element, this.events) };
	});

	describe("whith invalid element", function () {
		it("does nothing if element is undefined", function () {
			this.element = undefined;
			expect(this.subject).not.toThrow();
		});

		it("does nothing if element is null", function () {
			this.element = null;
			expect(this.subject).not.toThrow();
		});

		it("does nothing if element is false", function () {
			this.element = false;
			expect(this.subject).not.toThrow();
		});

		it("does nothing if element is 0", function () {
			this.element = 0;
			expect(this.subject).not.toThrow();
		});

		it("does nothing if element is empty string", function () {
			this.element = "";
			expect(this.subject).not.toThrow();
		});
	});

	describe("with valid element", function () {
		def("element", function () { return $("#plain") });

		beforeEach(function () {
			spyOn(this.element, "addEventListener");
		});

		it("adds event listeners for all events", function () {
			this.events = { click: $.noop, input: $.noop };
			this.subject();

			expect(this.element.addEventListener).toHaveBeenCalledWith("click", this.events.click);
			expect(this.element.addEventListener).toHaveBeenCalledWith("input", this.events.input);
		});

		it("adds single event listener for multiple events", function () {
			this.events = { "click input": $.noop };
			this.subject();

			expect(this.element.addEventListener).toHaveBeenCalledWith("click", this.events["click input"]);
			expect(this.element.addEventListener).toHaveBeenCalledWith("input", this.events["click input"]);
		});
	});
});
