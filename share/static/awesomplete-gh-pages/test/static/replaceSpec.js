describe("Awesomplete.REPLACE", function () {

	subject(function () { return Awesomplete.REPLACE });

	def("instance", function() { return { input: { value: "initial" } } });

	it("replaces input value", function () {
		this.subject.call(this.instance, { value: "JavaScript" });
		expect(this.instance.input.value).toBe("JavaScript");
	});
});
