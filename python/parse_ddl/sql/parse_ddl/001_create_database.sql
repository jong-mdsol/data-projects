USE [master]
GO
if exists (select * from sys.databases where name = 'parse_ddl')
BEGIN
	ALTER DATABASE [parse_ddl] SET SINGLE_USER;
	DROP DATABASE [parse_ddl];
END
GO
USE master
GO
CREATE DATABASE [parse_ddl]
GO

USE [parse_ddl]
GO

USE [parse_ddl]
GO
/****** Object:  View [dbo].[v_parse_ddl_objects_errors1]    Script Date: 9/29/2018 11:44:20 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create view [dbo].[v_parse_ddl_objects_errors1] as
select ddl, file_name, count(*) as count_new, min(git_tag) as min_git_tag, max(git_tag) as max_git_tag
from parse_ddl_objects 
where change_type = 'new'
group by ddl, file_name
having count(*) > 1
GO
/****** Object:  View [dbo].[v_parse_ddl_objects_errors2]    Script Date: 9/29/2018 11:44:20 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
create view [dbo].[v_parse_ddl_objects_errors2] as
select *
from parse_ddl_objects 
where object_type is null
GO
/****** Object:  Table [dbo].[all_tags]    Script Date: 9/29/2018 11:44:20 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[all_tags](
	[git_tag] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[git_compare_two_tags]    Script Date: 9/29/2018 11:44:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[git_compare_two_tags](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[full_path] [nvarchar](max) NULL,
	[dir_path] [nvarchar](max) NULL,
	[file_name] [nvarchar](255) NULL,
	[change_type] [nvarchar](255) NULL,
	[git_repo] [nvarchar](255) NULL,
	[git_tag1] [nvarchar](255) NULL,
	[git_tag2] [nvarchar](255) NULL,
 CONSTRAINT [PK_git_compare_two_tags] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[git_parse_ddl]    Script Date: 9/29/2018 11:44:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[git_parse_ddl](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[full_path] [nvarchar](max) NULL,
	[dir_path] [nvarchar](max) NULL,
	[file_name] [nvarchar](255) NULL,
	[file_content] [nvarchar](max) NULL,
	[file_content_hash] [nvarchar](255) NULL,
	[file_size] [bigint] NOT NULL,
	[ddls] [nvarchar](max) NULL,
	[git_repo] [nvarchar](255) NULL,
	[git_tag] [nvarchar](255) NULL,
 CONSTRAINT [PK_git_parse_ddl] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[git_parse_ddl_objects]    Script Date: 9/29/2018 11:44:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[git_parse_ddl_objects](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[full_path] [nvarchar](max) NULL,
	[dir_path] [nvarchar](max) NULL,
	[file_name] [nvarchar](255) NULL,
	[ddl] [nvarchar](max) NULL,
	[object_action] [nvarchar](50) NULL,
	[object_name] [nvarchar](255) NULL,
	[object_schema] [nvarchar](255) NULL,
	[object_type] [nvarchar](255) NULL,
	[git_repo] [nvarchar](255) NULL,
	[git_tag] [nvarchar](255) NULL,
 CONSTRAINT [PK_git_parse_ddl_objects] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[git_tag_dates]    Script Date: 9/29/2018 11:44:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[git_tag_dates](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[git_repo] [nvarchar](255) NULL,
	[git_tag] [nvarchar](255) NULL,
	[git_tag_date] [datetime] NULL,
 CONSTRAINT [PK_git_tag_dates] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[git_tag_exclusions]    Script Date: 9/29/2018 11:44:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[git_tag_exclusions](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[git_repo] [nvarchar](255) NULL,
	[git_tag] [nvarchar](255) NULL,
 CONSTRAINT [PK_git_tag_exclusions] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[parse_ddl]    Script Date: 9/29/2018 11:44:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[parse_ddl](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[full_path] [nvarchar](max) NULL,
	[dir_path] [nvarchar](max) NULL,
	[file_name] [nvarchar](255) NULL,
	[file_content] [nvarchar](max) NULL,
	[file_content_hash] [nvarchar](255) NULL,
	[file_size] [bigint] NOT NULL,
	[ddls] [nvarchar](max) NULL,
 CONSTRAINT [PK_parse_ddl] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[parse_ddl_objects]    Script Date: 9/29/2018 11:44:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[parse_ddl_objects](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[full_path] [nvarchar](max) NULL,
	[dir_path] [nvarchar](max) NULL,
	[file_name] [nvarchar](255) NULL,
	[ddl] [nvarchar](max) NULL,
	[object_action] [nvarchar](50) NULL,
	[object_name] [nvarchar](255) NULL,
	[object_schema] [nvarchar](255) NULL,
	[object_type] [nvarchar](255) NULL,
 CONSTRAINT [PK_parse_ddl_objects] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
USE [parse_ddl]
GO

/****** Object:  Table [dbo].[object_git_repo_refs]    Script Date: 10/17/2018 5:25:17 AM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[object_git_repo_refs](
	[object_name] [nvarchar](255) NOT NULL,
	[git_repo_refs] [nvarchar](400) NULL,
PRIMARY KEY CLUSTERED 
(
	[object_name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO


