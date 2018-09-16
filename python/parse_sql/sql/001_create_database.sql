USE [master]
GO
if exists (select * from sys.databases where name = 'parse_sql')
BEGIN
	ALTER DATABASE [parse_sql] SET SINGLE_USER;
	DROP DATABASE [parse_sql];
END
GO

CREATE DATABASE [parse_sql]
GO

USE [parse_sql]
GO
/****** Object:  Table [dbo].[all_tags]    Script Date: 9/15/2018 8:44:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[all_tags](
	[git_tag] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[parse_sql]    Script Date: 9/15/2018 8:44:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[parse_sql](
	[index] [bigint] NULL,
	[full_path] [varchar](max) NULL,
	[dir_path] [varchar](max) NULL,
	[file_name] [varchar](max) NULL,
	[file_content] [varchar](max) NULL,
	[file_content_hash] [varchar](max) NULL,
	[file_size] [bigint] NULL,
	[git_tag] [varchar](max) NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[git_sql_ddl]    Script Date: 9/15/2018 8:44:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[git_sql_ddl](
	[git_tag] [varchar](100) NOT NULL,
	[full_path] [varchar](500) NOT NULL,
	[ddl] [nvarchar](max) NOT NULL,
	[object_name] [nvarchar](255) NOT NULL,
 CONSTRAINT [PK_git_sql_ddl] PRIMARY KEY CLUSTERED 
(
	[git_tag] ASC,
	[full_path] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
/****** Object:  Table [dbo].[rave_version_git_tags]    Script Date: 9/15/2018 8:44:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[rave_version_git_tags](
	[rave_version] [nvarchar](255) NULL,
	[release] [nvarchar](255) NULL,
	[raveversionsortable1] [int] NULL,
	[raveversionsortable2] [int] NULL,
	[git_tag] [nvarchar](4000) NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[rave_version_prod_urls_git_tags]    Script Date: 9/15/2018 8:44:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[rave_version_prod_urls_git_tags](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[rave_version] [nvarchar](255) NULL,
	[release] [nvarchar](255) NULL,
	[raveversionsortable1] [int] NULL,
	[raveversionsortable2] [int] NULL,
	[git_tag] [nvarchar](4000) NULL,
 CONSTRAINT [PK_rave_version_prod_urls_git_tags] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  StoredProcedure [dbo].[checkdiff]    Script Date: 9/15/2018 8:44:25 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE procedure [dbo].[checkdiff] (@firsttag nvarchar(50), @secondtag nvarchar(50)) as
--declare @firsttag nvarchar(50) = 'v5.6.4-Patch1'
--declare @secondtag nvarchar(50) = 'v2015.1.0'
select subA.dir_path, subA.file_name, subB.dir_path, subB.file_name from
(select * from develop_branch_sql where git_tag = @firsttag and dir_path like '%Rave_Viper_Lucy%' and (dir_path like '%Daily%Changes%' or dir_path like '%procedures%' or dir_path like '%views%' or dir_path like '%functions%' or dir_path like '%types%')) subA
full outer join (select * from develop_branch_sql where git_tag = @secondtag and dir_path like '%Rave_Viper_Lucy%' and (dir_path like '%Daily%Changes%' or dir_path like '%procedures%' or dir_path like '%views%' or dir_path like '%functions%' or dir_path like '%types%')) subB on (subA.file_name = subB.file_name) or (subA.file_content_hash = subB.file_content_hash) 
where subA.file_content_hash is null or subB.file_content_hash is null or subA.file_content_hash <> subB.file_content_hash
GO
