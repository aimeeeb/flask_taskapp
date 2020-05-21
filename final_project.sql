create table if not exists CalendarItems
(
    ItemId int auto_increment
        primary key,
    Title  varchar(120) null,
    Date   datetime     null
);

create table if not exists Users
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

create table if not exists Events
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

create table if not exists Lists
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

create table if not exists Tasks
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

create
    definer = aimee@`%` procedure CreateEvent(IN title varchar(120), IN event_time datetime, IN user_id int)
BEGIN
    DECLARE exit handler for SQLEXCEPTION
        BEGIN
            ROLLBACK;
        END;

    START TRANSACTION;
    INSERT INTO CalendarItems(Title, Date) VALUES (title, event_time);
    INSERT INTO Events(CalendarItem, Creator) VALUES (LAST_INSERT_ID(), user_id);
    COMMIT;
END;

create
    definer = aimee@`%` procedure CreateList(IN list_title varchar(120), IN event_time datetime, IN user_id int)
BEGIN
    DECLARE exit handler for SQLEXCEPTION
        BEGIN
            ROLLBACK;
        END;

    START TRANSACTION;
    INSERT INTO CalendarItems(Title, Date) VALUES (list_title, event_time);
    INSERT INTO Lists(CalendarItem, Creator) VALUES (LAST_INSERT_ID(), user_id);
    COMMIT;
END;

create
    definer = aimee@`%` procedure CreateTask(IN list_title varchar(120), IN due_date datetime, IN info varchar(500),
                                             IN list_id int)
BEGIN
    DECLARE exit handler for SQLEXCEPTION
        BEGIN
            ROLLBACK;
        END;

    START TRANSACTION;
    INSERT INTO CalendarItems(Title, Date) VALUES (list_title, due_date);
    INSERT INTO Tasks(CalendarItem, Description, List) VALUES (LAST_INSERT_ID(), info, list_id);
    COMMIT;
END;


