---
author: Jacob Duijzer
date: 2019-03-07
tags: DDD, validation, async, Domain Driven Design
category: design
redirect: posts/async-model-validation/index 
---

# Asynchronous Model Validation

Last week I found some [great articles](http://www.kamilgrzybek.com/) about [Domain Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html). While I have been trying out various patterns and design principles like Clean Architecture and Domain Driven Design I was still finding out how to implement domain events. While doing some exercises I came up with a solution to validate domain entities with asynchronous validations which I want to share.

<!--more-->

I realize I have not written anything here for a while now. Just recently I started a new job and got quite busy with learning new projects. Just last week I found some interesting code I thought might be small but interesting to share in a new post to get started with blogging again. 

While I tried some of the sample code provided by [Kamil Grzybek](http://www.kamilgrzybek.com) I found this piece of [code](https://github.com/kgrzybek/sample-dotnet-core-cqrs-api/blob/master/src/SampleProject.Domain/Customers/Customer.cs).

```csharp
private Customer()
{
    this._orders = new List<Order>();
}

public Customer(
    string email, 
    string name, 
    ICustomerUniquenessChecker customerUniquenessChecker)
{
    this.Email = email;
    this.Name = name;

    var isUnique = customerUniquenessChecker.IsUnique(this);
    if (!isUnique)
        throw new BusinessRuleValidationException("Customer with this email already exists.");

    this.AddDomainEvent(new CustomerRegisteredEvent(this));
}
```

The thing is, I am using EF Core and I implemented every call in my repositories asynchronously. To check if a customer is unique or not I have to execute an asynchronous query which is not going to work in a constructor. I kept thinking about a proper solution to validate a business entity before actually creating it. After a few trials I came up with the following code:

```csharp
public class Customer
{
    private Customer(string email, string name)
    {
        Email = email;
        Name = name;
    }

    public string Email { get; private set; }
    public string Name { get; private set; }

    public static async Task<Customer> CreateNew(
        string email,
        string name,
        ICustomerUniquenessChecker customerUniquenessChecker)
    {
        if (!EmailValidator.IsValid(email))
            throw new BusinessRuleValidationException($"This email address is not valid: {email}");

        if (!NameValidator.IsValid(name))
            throw new BusinessRuleValidationException($"This name is not valid: {name}");

        var customer = new Customer(email, name);
        var isUnique = await customerUniquenessChecker.IsUnique(customer).ConfigureAwait(false);
        if (!isUnique)
            throw new BusinessRuleValidationException("Customer with this email already exists.");

        return customer;
    }
}

```

Now, when I want to create a new customer with a unique email address I can use the static method CreateNew in an asynchronous way:
```csharp        
public async Task SomeAsyncMethodInAService(string email, string name)
{
    try
    {
        var newCustomer = await Customer.CreateNew(
            email, 
            name, 
            _customerUniquenessChecker).ConfigureAwait(false);
    }
    catch(BusinessRuleValidationException ex)
    {
        // Do something or remove the try-catch
    }
}
```
By the way: I did not create an implementation of ICustomerUniquenessChecker, I used a mock in a test project (see the sample code on github)!

While it is nothing special I just like it and wanted to share it. Hope you liked it!

UPDATE: [Kamil Grzybek](www.kamilgrzybek.com/) commented on my article and pointed me in this direction: a blog post about [Async OOP 2: Constructors](http://blog.stephencleary.com/2013/01/async-oop-2-constructors.html) by [Stephen Cleary](http://blog.stephencleary.com).

### Links

* [Github source](https://github.com/jacobduijzer/AsynchronousEntityValidation)
* [Kamil Grzybek's Inspirational blog](www.kamilgrzybek.com/)
