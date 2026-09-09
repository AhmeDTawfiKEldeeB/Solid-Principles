# SOLID Principles

## What are SOLID Principles?

Imagine that you are building a small application.

At the beginning, everything looks simple.

You have a few classes, a few methods, and the code is easy to understand. 
Adding a new feature does not seem like a big deal.

But as the application grows, things start to change.

New features are added, existing requirements are modified, and more components
become connected to each other. A class that originally had a simple purpose
may slowly become responsible for many different things.

Now a small change can require modifying multiple parts of the codebase.
One change may introduce unexpected bugs somewhere else, and adding new
features becomes harder than it should be.

This is where **SOLID** becomes useful.

**SOLID** is an acronym for five fundamental design principles that help
developers build software that is easier to maintain, extend, and test.

The five principles are:

- **S** — Single Responsibility Principle
- **O** — Open/Closed Principle
- **L** — Liskov Substitution Principle
- **I** — Interface Segregation Principle
- **D** — Dependency Inversion Principle

These principles are not strict rules that every piece of code must follow.
Instead, they provide guidelines for designing software that can evolve
without becoming unnecessarily complicated.

---

## Why Learn SOLID?

The purpose of SOLID is not to make the code more complicated by adding
classes and abstractions everywhere.

The goal is to make the code easier to change **when change is actually
needed**.

Throughout this repository, each principle will be introduced through a
practical problem:

```text
Problem
   ↓
Understand the consequences
   ↓
Apply the principle
   ↓
Refactor the design
   ↓
Compare the result
   ↓
Extract practical rules
```

---

## The Story Behind This Repository

To make these principles easier to understand, this repository follows the
development of a simple **e-commerce system**.

We will start with a straightforward implementation.

At first, the system will work perfectly.

Then, just like a real project, new requirements will appear.

We will add new features, introduce new types of products, change existing
behavior, and connect different parts of the system.

With each change, we will encounter a different design problem.

Instead of simply explaining the solution, we will first look at the problem,
understand why it happens, and then refactor the code using one of the SOLID
principles.

The goal is not only to learn what each principle means, but also to
understand **when it becomes useful and what problems it helps prevent**.

---

## The Journey

We will build the system step by step:

### 01 — Single Responsibility Principle

We start with a simple product class.

As the system grows, the class begins handling multiple responsibilities.
We will see why this makes the code harder to maintain and how separating
responsibilities makes the design cleaner.

📁 **Chapter Readme**: [solid_principles/single_responsibility/README.md](solid_principles/single_responsibility/README.md)

### 02 — Open/Closed Principle

The store needs to support new types of products.

We will first see how adding new behavior can force us to modify existing code,
and then redesign the system so new behavior can be added without changing
the existing implementation.

### 03 — Liskov Substitution Principle

As different product types are introduced, we need to make sure that
subclasses behave consistently with their base class.

We will see what happens when a subclass violates the expectations of its
parent and why this can lead to unexpected behavior.

### 04 — Interface Segregation Principle

Different products do not necessarily support the same operations.

Instead of forcing every product to implement functionality it does not need,
we will break large interfaces into smaller, more focused ones.

### 05 — Dependency Inversion Principle

Finally, the system starts depending on external services such as storage
and notifications.

We will see why directly depending on concrete implementations makes the
system harder to change, and how abstractions and dependency injection can
make the design more flexible.