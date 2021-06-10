---
author: Jacob Duijzer
date: 2018-08-07
tags: MvvmCross, MediatR, CQRS, Clean Architecture, Xamarin, Xamarin Forms
category: Xamarin
redirect: posts/mvvmcross_with_mediatr/index 
---

# Using MediatR in an MvvmCross App

A while ago I was listening to a podcast from [DotNetRocks](https://www.dotnetrocks.com/?show=1538) about [Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html). Around the same time I read something about a [Clean Architecture template](https://github.com/ardalis/CleanArchitecture) which happens to be from [Steve Smith](https://github.com/ardalis), the same guy talking about it on the DotNetRocks show. 

<!--more-->

After doing quite some reading about Clean Architecture I created some sample apps to try different patterns and I really liked it! I was lucky as I was just starting a new project from scratch and decided to implement "Clean Architecture". In this post I will explain how I am using [CQRS](https://martinfowler.com/bliki/CQRS.html) (or Command Query Responsibility Segregation). CQRS  one of the many ways to create cleaner architectures and cleaner code. CQRS is one of the many patterns used to create a cleaner architecture. Basically you create a seperation between Commands (alter the state of your application) and Queries (get information from your application). 

I am not going into the details of the patterns. I am planning to write more posts about [Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html) and how I am using it with Xamarin but feel free and start reading the links at the end of this post to learn more about the theory and the details!

# First learning

In the beginning of my journey I copied some code from a [clean architecture sample](https://github.com/stephanhoekstra/clean-architecture) belonging to a nice [post](https://medium.com/@stephanhoekstra/clean-architecture-in-net-8eed6c224c50) about Clean Architecture. These were the (base)classes to create handlers and get response and started to reuse it in different test projects. After copying it for the 3rd time I decided to create a nuget package but just after releasing the first version to nuget I stumbled upon [MediatR](https://github.com/jbogard/MediatR). Basically the same code but with much more features and better implemented.


# Let's start


Let's just start with a simple example: a login page where a user needs to enter credentials, which, after being validated, will be send to a web service. 

#### ViewModel

The ViewModel has an injected object, IMediator. The Mediator looks into the IoC container for the correct handler and handles messages as you can see in the 'LoginAsync' method.


```csharp
public class LoginViewModel : BaseViewModel
{
    private readonly IMediator _mediator;

    public LoginViewModel(IMediator mediator)
    {
        _mediator = mediator;
    }

    public IMvxAsyncCommand LoginCommand => new MvxAsyncCommand(LoginAsync, () => CanLogin);

    private string _username;
    public string Username
    {
        get => _username;
        set { SetProperty(ref _username, value); RaisePropertyChanged(() => CanLogin); }
    }

    private string _password;
    public string Password
    {
        get => _password;
        set { SetProperty(ref _password, value); RaisePropertyChanged(() => CanLogin); }
    }

    private string _errorMessage;
    public string ErrorMessage
    {
        get => _errorMessage;
        private set => SetProperty(ref _errorMessage, value);
    }

    public bool CanLogin => !string.IsNullOrEmpty(Username) && Username.Length >= 5 &&
                                   !string.IsNullOrEmpty(Password) && Password.Length >= 4;
    
    private async Task LoginAsync()
    {
        var result = await _mediator.Send(LoginRequest.WithCredentials(Username, Password))
                                    .ConfigureAwait(false);

        if (result.Succes)
            await NavigationService.Navigate<StartViewModel>()
                                   .ConfigureAwait(false);
        else
            ErrorMessage = result.Message;
    }
}
```

#### LoginHandler

The LoginHandler is where the real execution happens. The handler is supposed to be a mediator between the core or the domain and the outside world. In Clean Architecture this is often referred to as a **UseCase**.

```csharp
public class LoginHandler : IRequestHandler<LoginRequest, LoginResponse>
{
    private readonly ILoginService _loginService;

    public LoginHandler(ILoginService loginService)
    {
        _loginService = loginService;
    }

    public async Task<LoginResponse> Handle(LoginRequest request, CancellationToken cancellationToken)
    {
        try
        {
            var result = await _loginService.LoginAsync(request.Username, request.Password)
                                            .ConfigureAwait(false);

            return LoginResponse.WithStatus(result);
        }
        catch (System.Exception ex)
        {
            return LoginResponse.WithStatusAndMessage(false, ex.Message);
        }
    }
}
```

#### LoginRequest

I use the request to send the login credentials to the mediator. A Request could also be an empty object as we will see later on.

```csharp
public class LoginRequest : IRequest<LoginResponse>
{
    public string Username { get; }

    public string Password { get; }
    
    private LoginRequest(string username, string password)
    {
        Username = username;

        Password = password;
    }

    public static LoginRequest WithCredentials(string username, string password)
    => new LoginRequest(username, password);
}
```

#### LoginResponse
Just a response to know if our credentials were correct so we can continue.

```csharp
public class LoginResponse
{
    public bool Succes { get; }

    public string Message { get; }

    private LoginResponse(bool success) => Succes = success;

    private LoginResponse(bool success, string message) 
        : this(success) => Message = message;

    public static LoginResponse WithStatus(bool success) 
    => new LoginResponse(success);

    public static LoginResponse WithStatusAndMessage(bool success, string message) 
    => new LoginResponse(success, message);
}
```

Please download the [GitHub sample project](https://github.com/jacobduijzer/MvvmCrossWithMediatR) to see the views and run the sample! 


# Clean, testable code 

The view model has just a few lines of code to tie things together, all logic is handled at a deeper level. The handlers are just small classes to handle specific parts of the login (hence the name UseCase). Everything is injected with Interfaces so everything is loosely coupled. This makes it very easy to write unit tests and cover a large part of your app logic. Just have a look at the test project in the [GitHub sample project](https://github.com/jacobduijzer/MvvmCrossWithMediatR) to see how much of the code is tested.

# Issues with MediatR

I started using MediatR without the actual mediator but by calling the handlers straight in my viewmodels. Although this can be done it needs more lines of code. I really got into trouble when I wanted to implement a command though (a request without a response). By overriding AsyncHandler<T> I lost the possibility to call Handle() myself. Just after looking into the code and the usage of the IMediator / Mediator I discovered the real beauty of MediatR. My code just became even more cleaner!

But how sad were my first experiences. I almost gave up on it completely. There is some documentation about MediatR, together with some samples and there is some documentation about MvvmCross but I really got into some detailed code issues here.

I had to dive into the source of Mediatr, MvvmCross and Autofac to get a grasp of what was happening. And although I got it working, I still have to do some more investigating to find out what the real problem is. Anyway, this is how I got it working:

The ServiceFactory is responsible for resolving the handlers from the IoC container. You create a generic factory so MediatR can work with all kind of IoC containers to resolve handlers. It seems like all containers (e.g. AutoFac, AspNetCore, Ninject, etc) are return an empty array when no object is found but MvvmCross throws an Exception. I wrote about this in the [README](https://github.com/jacobduijzer/MvvmCrossWithMediatR/blob/master/README.md) of the sample!

Anyway, I am using it now and this seems to work:

```csharp
CreatableTypes()
                .EndingWith("Handler")
                .AsInterfaces()
                .RegisterAsLazySingleton();
                
Mvx.LazyConstructAndRegisterSingleton<IMediator, Mediator>();

Mvx.RegisterSingleton<ServiceFactory>((Type serviceType) =>
{
    var resolver = Mvx.Resolve<IMvxIoCProvider>();

    try
    {
        return resolver.Resolve(serviceType);
    }
    catch (Exception)
    {
        // a "bit" buggy, I know!
        return Array.CreateInstance(serviceType.GenericTypeArguments[0], 0);
    }
});
```

It is a good practice to start testing with .RegisterAsSingleton() instead of Lazy because I got into a lot of vague issues when there are issues with constructing the viewmodels.

Also, registering types instead of singletons gave me issues, the ServiceFactory wasn't able to construct my empty array anymore.

# More handlers

Just for the fun of it, let's add two more handlers, two handlers from the MediatR samples:

#### OneWayHandler
```csharp
public class OneWayHandler : AsyncRequestHandler<OneWay>
{
    public OneWayHandler()
    {
    }

    protected override Task Handle(OneWay request, CancellationToken cancellationToken)
    {
        System.Diagnostics.Debug.WriteLine(request.Message);

        return Task.FromResult(true);
    }
}
```

#### PingHandler
```
public class PingHandler : IRequestHandler<Ping, Pong>
{
    public PingHandler()
    {
    }

    public async Task<Pong> Handle(Ping request, CancellationToken cancellationToken)
    {
        return await Task.FromResult(new Pong { Message = request.Message + " Pong" });
    }
}
```

# Finally

There is a lot more that can be done with [MediatR](https://github.com/jbogard/MediatR), much more to tell about [CQRS](https://martinfowler.com/bliki/CQRS.html) and t [Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html) and I am planning to write at least one more post about my experiences with all this with Xamarin but in the meantime check the source on [GitHub](https://github.com/jacobduijzer/MvvmCrossWithMediatR). And don't forget to tell me if you learned something. Any plans to try it out yourself? Having questions? Add a comment or contact me in the [Xamarin Slack](https://xamarinchat.herokuapp.com/)!

# Links

* [GitHub sample project](https://github.com/jacobduijzer/MvvmCrossWithMediatR)
* [MediatR](https://github.com/jbogard/MediatR)
* [CQRS](https://martinfowler.com/bliki/CQRS.html)
* [Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html)
* [A Clean Architecture in .NET](https://medium.com/@stephanhoekstra/clean-architecture-in-net-8eed6c224c50)
* [DotNetRocks](https://www.dotnetrocks.com/?show=1538)
* [MvvmCross](https://www.mvvmcross.com)