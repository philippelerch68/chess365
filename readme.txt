


@philippe

ANALYSE
=======


    GAMES FOLDERS
    *************
    - 200 files
    - Keys :['Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result', 'WhiteElo', 'BlackElo', 'ECO', 'game']

    Event : String (location) 
    Site : String ( Country)
    Date : String YYY.MM.DD  ! to be transformed on ISO !
    Round : Integer
    White : String (First name, Name)  coma separed
    Black : String (First name, Name)  coma separed
    Result : String 
    WhiteElo : Integer
    BlackElo : Integer
    ECO : String
    Game : Data play history.


    PLAYERS
    *******
    - 200 files
    - Keys : ['Rank', 'Name', 'ELO', 'Title', 'FIDEId', 'Federation', 'Games', 'BirthYear', 'Page']
    
    Rank : Integer
    Name : String (First Name LastName) space separed
    ELO : 
    Title : String
    FIDEId :
    Federation : 
    Games : 
    BirthYear : String year
    Page : URL


TABLES
*******

Country
------
    id
    *Name (PK) String
    *Code String()

Cities
------
    id (PK)Int
    Cities String 
    County_id (Fk) Int

Location
--------
    id (PK) Int
    *place_name (event) String
    *city_id (Site) (FK) Int
    County_id (FK) Int


Events
-------
    id (PK)
    *Location_id
    *Date

Title
------
    Id (PK)
    Title (String)

Federation
----------
    id (PK)
    Name (String)


Game_partie
-----------
    Location_id 
    Event_id


PLAYERS
---------
    id (PK)
    Firstname (String)
    LastName (String)
    BirthYear (Date YYYY)
    Federation_id(FK)
    FIDEId (Fk)
    Rank (Int)
    Title_id (FK)
    Page (string) (URL)
    ELO
    Games


Round
------
id (PK)
*Round (Int)
*White (Players_id)
*Black (Players_id)
Result (String)
WhiteElo (Int)
BlackElo (Int)
ECO (String)
game (BLOC)



















