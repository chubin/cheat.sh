describe("Awesomplete.DATA", function () {

	subject(function () { return Awesomplete.DATA(this.item) });

	it("returns original String", function () {
		this.item = "JavaScript";
		expect(this.subject).toEqual("JavaScript");
	});

	it("returns original Object", function () {
		this.item = { label: "JavaScript", value: "JS" };
		expect(this.subject).toEqual({ label: "JavaScript", value: "JS" });
	});

	it("returns original Array", function () {
		this.item = [ "JavaScript", "JS" ];
		expect(this.subject).toEqual([ "JavaScript", "JS" ]);
	});
});
