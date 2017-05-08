describe("awesomplete.open", function () {

	$.fixture("plain");

	subject(function () { return new Awesomplete("#plain", { list: ["item1", "item2", "item3"] }) });

	// Exposes this bug https://github.com/LeaVerou/awesomplete/pull/16740
	// FIXME better fix is probably required as discussed in PR above
	xit("fills in the list on creation", function () {
		$("#plain").value = "ite";
		this.subject.open();

		expect(this.subject.ul.children.length).toBe(3);
	});

	it("opens completer", function () {
		this.subject.open();
		expect(this.subject.ul.hasAttribute("hidden")).toBe(false);
	});

	describe("with autoFirst: true", function () {
		beforeEach(function () {
			this.subject.autoFirst = true;
			spyOn(this.subject, "goto");
		});

		it("selects first item if wasn't seleted before", function () {
			this.subject.open();

			expect(this.subject.goto).toHaveBeenCalledWith(0);
		});

		it("does not select any item if was seleted before", function () {
			this.subject.index = 0;
			this.subject.open();

			expect(this.subject.goto).not.toHaveBeenCalled();
		});
	});

	describe("with autoFirst: false", function () {
		it("does not select any item", function () {
			this.subject.autoFirst = false;
			spyOn(this.subject, "goto");

			this.subject.open();

			expect(this.subject.goto).not.toHaveBeenCalled();
		});
	});

	it("fires awesomplete-open event", function () {
		var handler = $.spyOnEvent(this.subject.input, "awesomplete-open");

		this.subject.open();

		expect(handler).toHaveBeenCalled();
	});
});
