describe("Awesomplete list", function () {

	$.fixture("options");

	subject(function () { return new Awesomplete(this.element, this.options) });

	def("element", "#no-options");

	it("is empty if not provided", function () {
		expect(this.subject._list).toEqual([]);
	});

	describe("setter", function () {
		it("assigns from array", function () {
			this.subject.list = [ "From", "Array" ];
			expect(this.subject._list).toEqual([ "From", "Array" ]);
		});

		it("assigns from comma separated list", function () {
			this.subject.list = "From, Inline, List";
			expect(this.subject._list).toEqual([ "From", "Inline", "List" ]);
		});

		it("assigns from element specified by selector", function () {
			this.subject.list = "#data-list";
			expect(this.subject._list).toEqual([
				{ label: "With", value: "With" },
				{ label: "Data", value: "Data" },
				{ label: "List", value: "List" }
			]);
		});

		it("assigns from element", function () {
			this.subject.list = $("#data-list");
			expect(this.subject._list).toEqual([
				{ label: "With", value: "With" },
				{ label: "Data", value: "Data" },
				{ label: "List", value: "List" }
			]);
		});

		it("does not assigns from not found list", function () {
			this.subject.list = "#nosuchlist";
			expect(this.subject._list).toEqual([]);
		});

		it("does not assigns from empty list", function () {
			this.subject.list = "#empty-list";
			expect(this.subject._list).toEqual([]);
		});

		describe("with active input", function() {
			beforeEach(function() {
				this.subject.input.focus();
			});

			it("evaluates completer", function() {
				spyOn(this.subject, "evaluate");
				this.subject.list = "#data-list";

				expect(this.subject.evaluate).toHaveBeenCalled();
			});
		});
	});

	describe("constructor option", function () {
		it("assigns from array", function () {
			this.options = { list: [ "From", "Array" ] };
			expect(this.subject._list).toEqual([ "From", "Array" ]);
		});

		it("assigns from comma separated list", function () {
			this.options = { list: "From, Inline, List" };
			expect(this.subject._list).toEqual([ "From", "Inline", "List" ]);
		});

		it("assigns from element specified by selector", function () {
			this.options = { list: "#data-list" };
			expect(this.subject._list).toEqual([
				{ label: "With", value: "With" },
				{ label: "Data", value: "Data" },
				{ label: "List", value: "List" }
			]);
		});

		it("assigns from list specified by element", function () {
			this.options = { list: $("#data-list") };
			expect(this.subject._list).toEqual([
				{ label: "With", value: "With" },
				{ label: "Data", value: "Data" },
				{ label: "List", value: "List" }
			]);
		});
	});

	describe("data-list html attribute", function () {
		it("assigns from comma separated list", function () {
			this.element = "#with-data-list-inline";
			expect(this.subject._list).toEqual(["With", "Data", "List", "Inline"]);
		});

		it("assigns from element referenced by selector", function () {
			this.element = "#with-data-list";
			expect(this.subject._list).toEqual([
				{ label: "With", value: "With" },
				{ label: "Data", value: "Data" },
				{ label: "List", value: "List" }
			]);
		});
	});

	describe("list html attribute", function () {
		it("assigns from element referenced by id", function () {
			this.element = "#with-list";
			expect(this.subject._list).toEqual([
				{ label: "With", value: "With" },
				{ label: "List", value: "List" }
			]);
		});
	});
});
