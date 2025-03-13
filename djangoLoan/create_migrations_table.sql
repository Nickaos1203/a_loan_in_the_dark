CREATE TABLE [django_migrations] (
    [id] int IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [app] nvarchar(255) NOT NULL,
    [name] nvarchar(255) NOT NULL,
    [applied] datetime NOT NULL
);