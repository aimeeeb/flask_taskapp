create table CalendarItems
(
    ItemId int auto_increment
        primary key,
    Title  varchar(120) null,
    Date   datetime     null
);

create table Events
(
    EventId      int auto_increment
        primary key,
    CalendarItem int          null,
    Description  varchar(500) null,
    Creator      int          null,
    constraint Events_ibfk_1
        foreign key (CalendarItem) references CalendarItems (ItemId),
    constraint Events_ibfk_2
        foreign key (Creator) references Users (UserId)
);

create index CalendarItem
    on Events (CalendarItem);

create index Creator
    on Events (Creator);

create table Lists
(
    ListId       int auto_increment
        primary key,
    CalendarItem int        null,
    Creator      int        null,
    Complete     tinyint(1) null,
    Deleted      datetime   null,
    constraint Lists_ibfk_1
        foreign key (CalendarItem) references CalendarItems (ItemId),
    constraint Lists_ibfk_2
        foreign key (Creator) references Users (UserId)
);

create index CalendarItem
    on Lists (CalendarItem);

create index Creator
    on Lists (Creator);

create table Tasks
(
    TaskId       int auto_increment
        primary key,
    CalendarItem int          null,
    List         int          null,
    Description  varchar(500) null,
    Complete     tinyint(1)   null,
    Deleted      datetime     null,
    constraint Tasks_ibfk_1
        foreign key (CalendarItem) references CalendarItems (ItemId),
    constraint Tasks_ibfk_2
        foreign key (List) references Lists (ListId)
);

create index CalendarItem
    on Tasks (CalendarItem);

create index List
    on Tasks (List);

create table Users
(
    UserId   int auto_increment
        primary key,
    Username varchar(20)  not null,
    Email    varchar(120) not null,
    Password varchar(60)  not null,
    Deleted  datetime     null,
    constraint unique_email
        unique (Email),
    constraint unique_username
        unique (Username)
);