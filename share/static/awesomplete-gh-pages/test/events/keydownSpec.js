describe("keydown event", function () {

	$.fixture("plain");

	subject(function () {
		return new Awesomplete("#plain", { list: ["item1", "item2", "item3"] });
	});

	beforeEach(function () {
		$.type(this.subject.input, "ite");
	});

	it("supports enter", function () {
		this.subject.next();

		spyOn(this.subject, "select");
		$.keydown(this.subject.input, $.k.ENTER);

		expect(this.subject.select).toHaveBeenCalled();
	});

	it("supports escape", function () {
		spyOn(this.subject, "close");
		$.keydown(this.subject.input, $.k.ESC);

		expect(this.subject.close).toHaveBeenCalledWith({
			reason: "esc"
		});
	});

	it("supports down arrow", function () {
		spyOn(this.subject, "next");
		$.keydown(this.subject.input, $.k.DOWN);

		expect(this.subject.next).toHaveBeenCalled();
	});

	it("supports up arrow", function () {
		spyOn(this.subject, "previous");
		$.keydown(this.subject.input, $.k.UP);

		expect(this.subject.previous).toHaveBeenCalled();
	});

	it("ignores other keys", function() {
		spyOn(this.subject, "select");
		spyOn(this.subject, "close");
		spyOn(this.subject, "next");
		spyOn(this.subject, "previous");

		$.keydown(this.subject.input, 111);

		expect(this.subject.select).not.toHaveBeenCalled();
		expect(this.subject.close).not.toHaveBeenCalled();
		expect(this.subject.next).not.toHaveBeenCalled();
		expect(this.subject.previous).not.toHaveBeenCalled();
	});

	it("does nothing if not opened", function () {
		this.subject.close();

		spyOn(this.subject, "next");
		$.keydown(this.subject.input, $.k.DOWN);

		expect(this.subject.next).not.toHaveBeenCalled();
	});
});
