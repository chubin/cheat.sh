describe("awesomplete.close", function () {

	$.fixture("plain");

	subject(function () { return new Awesomplete("#plain", { list: ["item1", "item2", "item3"] }) });

	beforeEach(function () {
		$.type(this.subject.input, "ite");
		this.subject.open();
		this.subject.next();
	});

	it("closes completer", function () {
		this.subject.close();
		expect(this.subject.ul.hasAttribute("hidden")).toBe(true);
	});

	it("makes no item selected", function () {
		this.subject.close();
		expect(this.subject.index).toBe(-1);
	});

	it("fires awesomplete-close event", function () {
		var handler = $.spyOnEvent(this.subject.input, "awesomplete-close");
		this.subject.close();

		expect(handler).toHaveBeenCalledWith(
			jasmine.any(document.createEvent("HTMLEvents").constructor)
		);
	});

	it("returns early if already closed", function () {
		var handler = $.spyOnEvent(this.subject.input, "awesomplete-close");
		this.subject.close();
		this.subject.close();

		expect(handler.calls.count()).toBe(1);
	});
});
