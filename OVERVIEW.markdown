Overview of the new architecture.
=================================

Being a complete redesign of the point of sale system, a bunch of things have
changed. Specifically, we're now going for a modular system with the intent of
selling it.

Modules
-------

* Point of Sale: the core of the product -- a system that enables you to create
  saleable items and simple discounts (per-item, percentage and flat) with
  optional sales tax that get rung up. Generates receipts as well.
* Credit card processing. Possibly through square
* Mobile integration.
* Donations: Take donations at POS and track them for accounting purposes.
* Sales/Discounts: Define sales (such as the dollar sale) without having to
  duplicate items, etc.
* Inventory Control: Track incoming/outgoing inventory simply and easily.
* **STRETCH** Port something like sawzall to the the mapreduce framework so that
  we can dynamically create mapreduces.