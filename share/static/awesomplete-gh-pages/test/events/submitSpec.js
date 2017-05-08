describe("form submit event", function () {

	$.fixture("options");

	subject(function () {	return new Awesomplete("#inside-form") });

	it("closes completer", function () {
		spyOn(Awesomplete.prototype, "close");
		// prevent full page reload in Firefox, which causes tests to stop running
		$.on(this.subject.input.form, "submit", function (evt) { evt.preventDefault() });
		$.fire(this.subject.input.form, "submit");
		expect(Awesomplete.prototype.close).toHaveBeenCalledWith(
			{ reason: "submit" },
			jasmine.any(document.createEvent("HTMLEvents").constructor)
		);
	});
});
