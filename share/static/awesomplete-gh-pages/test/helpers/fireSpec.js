describe("Awesomplete.$.fire", function () {

	$.fixture("plain");

	subject(function () {
		return Awesomplete.$.fire.bind(Awesomplete.$, this.element);
	});

	def("element", function () { return $("#plain") });

	beforeEach(function () {
		spyOn(this.element, "dispatchEvent");
	});

	it("fires event once", function () {
		this.subject("click");
		expect(this.element.dispatchEvent.calls.count()).toEqual(1);
	});

	describe("fires different event types", function () {
		it("fires click event", function () {
			this.subject("click");
			expect(this.element.dispatchEvent).toHaveBeenCalledWith(jasmine.objectContaining({ type: "click" }));
		});

		it("fires input event", function () {
			this.subject("input");
			expect(this.element.dispatchEvent).toHaveBeenCalledWith(jasmine.objectContaining({ type: "input" }));
		});
	});

	describe("sets event properties", function () {
		it("makes cancelable event", function () {
			this.subject("click");
			expect(this.element.dispatchEvent).toHaveBeenCalledWith(jasmine.objectContaining({ cancelable: true }));
		});

		it("can't make non cancelable event", function () {
			this.subject("click", { cancelable: false });
			expect(this.element.dispatchEvent).toHaveBeenCalledWith(jasmine.objectContaining({ cancelable: true }));
		});

		it("makes event that bubbles", function () {
			this.subject("click");
			expect(this.element.dispatchEvent).toHaveBeenCalledWith(jasmine.objectContaining({ bubbles: true }));
		});

		it("can't make event that does not bubble", function () {
			this.subject("click", { bubbles: false });
			expect(this.element.dispatchEvent).toHaveBeenCalledWith(jasmine.objectContaining({ bubbles: true }));
		});

		it("sets properties on the event", function () {
			var properties = { text: "hello", preventDefault: $.noop };

			this.subject("click", properties);
			expect(this.element.dispatchEvent).toHaveBeenCalledWith(jasmine.objectContaining(properties));
		});
	});
});
