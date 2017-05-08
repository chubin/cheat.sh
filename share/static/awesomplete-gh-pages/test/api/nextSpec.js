describe("awesomplete.next", function () {

	$.fixture("plain");

	subject(function () {
		return new Awesomplete("#plain", { list: ["item1", "item2", "item3"] });
	});

	def("lastIndex", function () { return this.subject.ul.children.length - 1 });

	describe("without any items found", function () {
		beforeEach(function () {
			$.type(this.subject.input, "nosuchitem");
			this.subject.open();
		});

		it("does not select any item", function () {
			this.subject.next();
			expect(this.subject.index).toBe(-1);
		});
	});

	describe("with some items found", function () {
		beforeEach(function () {
			$.type(this.subject.input, "ite");
			this.subject.open();
		});

		describe("and no item was already selected", function () {
			it("selects the first item ", function () {
				this.subject.next();
				expect(this.subject.index).toBe(0);
			});
		});

		describe("and some item was already selected", function () {
			it("selects the second item", function () {
				this.subject.goto(0);
				this.subject.next();
				expect(this.subject.index).toBe(1);
			});

			it("selects the last item", function () {
				this.subject.goto(this.lastIndex - 1);
				this.subject.next();
				expect(this.subject.index).toBe(this.lastIndex);
			});

			it("selects the first item after reaching the end", function () {
				this.subject.goto(this.lastIndex);
				this.subject.next();
				expect(this.subject.index).toBe(0);
			});
		});
	});
});
