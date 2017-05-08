describe("input event", function () {

	$.fixture("plain");

	subject(function () { return new Awesomplete("#plain") });

	it("rebuilds the list", function () {
		spyOn(Awesomplete.prototype, "evaluate");
		$.type(this.subject.input, "ite");
		expect(Awesomplete.prototype.evaluate).toHaveBeenCalled();
	});
});
