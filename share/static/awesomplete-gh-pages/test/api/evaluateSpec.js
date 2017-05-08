describe("awesomplete.evaluate", function () {

	$.fixture("plain");

	subject(function () {
		return new Awesomplete("#plain", { list: ["item1", "item2", "item3"] });
	});

	describe("with too short input value", function () {
		beforeEach(function () {
			$.type(this.subject.input, "i");
		});

		it("closes completer", function () {
			spyOn(this.subject, "close");
			this.subject.evaluate();

			expect(this.subject.close).toHaveBeenCalledWith({
				reason: "nomatches"
			});
		});
	});

	describe("with no items found", function () {
		beforeEach(function () {
			$.type(this.subject.input, "nosuchitem");
		});

		it("closes completer", function () {
			spyOn(this.subject, "close");
			this.subject.evaluate();

			expect(this.subject.close).toHaveBeenCalledWith({
				reason: "nomatches"
			});
		});
	});

	describe("with some items found", function () {
		beforeEach(function () {
			$.type(this.subject.input, "ite");
		});

		it("opens completer", function () {
			spyOn(this.subject, "open");
			this.subject.evaluate();

			expect(this.subject.open).toHaveBeenCalled();
		});

		it("fills completer with found items", function () {
			this.subject.evaluate();
			expect(this.subject.ul.children.length).toBe(3);
		});

		it("shows no more than maxItems", function () {
			this.subject.maxItems = 2;
			this.subject.evaluate();
			expect(this.subject.ul.children.length).toBe(2);
		});

		it("makes no item selected", function () {
			this.subject.evaluate();
			expect(this.subject.index).toBe(-1);
		});
	});

	describe("with minChars: 0", function () {
		beforeEach(function () {
			this.subject.minChars = 0;
		});

		it("opens completer", function () {
			spyOn(this.subject, "open");
			this.subject.evaluate();

			expect(this.subject.open).toHaveBeenCalled();
		});

		it("fills completer with all items", function () {
			this.subject.evaluate();
			expect(this.subject.ul.children.length).toBe(3);
		});

		it("shows no more than maxItems", function () {
			this.subject.maxItems = 2;
			this.subject.evaluate();
			expect(this.subject.ul.children.length).toBe(2);
		});

		it("makes no item selected", function () {
			this.subject.evaluate();
			expect(this.subject.index).toBe(-1);
		});
	});
});
