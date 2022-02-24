import re

from fuzzywuzzy import fuzz, process

address_list = [('777 Brockton Avenue, Abington MA 2351', 'Brockton Avenue, Abington 2351 MA 777'),
                ('30 Memorial Drive, Avon MA 2322', 'Avon Memorial Drive, 2322 30 MA'),
                ('250 Hartford Avenue, Bellingham MA 2019', '250 Bellingham Avenue, 2019 MA Hartford'),
                ('700 Oak Street, Brockton MA 2301', 'Street, MA 700 Brockton Oak 2301'),
                ('66-4 Parkhurst Rd, Chelmsford MA 1824', '66-4 MA Rd, Parkhurst 1824 Chelmsford'),
                ('591 Memorial Dr, Chicopee MA 1020', 'MA 1020 Chicopee 591 Memorial Dr,'),
                ('55 Brooksby Village Way, Danvers MA 1923', '1923 Village Way, 55 MA Danvers Brooksby'),
                ('137 Teaticket Hwy, East Falmouth MA 2536', '137 Hwy, 2536 Teaticket Falmouth MA East'),
                ('42 Fairhaven Commons Way, Fairhaven MA 2719', '2719 MA Way, Fairhaven 42 Fairhaven Commons'),
                ('374 William S Canning Blvd, Fall River MA 2721', '374 River William Fall S Blvd, MA Canning 2721'),
                ('121 Worcester Rd, Framingham MA 1701', 'Framingham 101 MA Rd, 121 Worcester'),
                ('677 Timpany Blvd, Gardner MA 1440', 'MA 677 1440 Blvd, Timpany Gardner'),
                ('337 Russell St, Hadley MA 1035', 'Hadley 337 Russell 1035 MA St,'),
                ('295 Plymouth Street, Halifax MA 2338', 'Street, 2338 MA 295 Plymouth Halifax'),
                ('1775 Washington St, Hanover MA 2339', 'Washington St, 1775 Hanover MA 2339'),
                ('280 Washington Street, Hudson MA 1749', 'Washington 1749 Street, Hudson MA 280'),
                ('20 Soojian Dr, Leicester MA 1524', 'Leicester 1524 Dr, 20 MA Soojian'),
                ('11 Jungle Road, Leominster MA 1453', 'Leominster MA 11 Jungle 1453 Road,'),
                ('301 Massachusetts Ave, Lunenburg MA 1462', 'Lunenburg 301 Massachusetts Ave, MA 1462'),
                ('780 Lynnway, Lynn MA 1905', '780 Lynn 1905 Lynnway, MA'),
                ('70 Pleasant Valley Street, Methuen MA 1844', 'Pleasant Street, Valley 70 MA Methuen 1844'),
                ('830 Curran Memorial Hwy, North Adams MA 1247', 'North Memorial 830 Adams MA Curran Hwy, 1247'),
                ('1470 S Washington St, North Attleboro MA 2760', '1470 St, S Attleboro MA 2760 Washington North'),
                ('506 State Road, North Dartmouth MA 2747', 'Dartmouth State 506 2747 MA Road, North'),
                ('742 Main Street, North Oxford MA 1537', '742 Main Oxford 1537 North Street, MA'),
                ('72 Main St, North Reading MA 1864', '72 North MA 1864 Main Reading St,'),
                ('200 Otis Street, Northborough MA 1532', 'MA 1532 Otis 200 Northborough Street,'),
                ('180 North King Street, Northhampton MA 1060', 'Northhampon North King MA 180 Street, 1060'),
                ('555 East Main St, Orange MA 1364', 'East Orange Main St, 1364 MA 555'),
                ('555 Hubbard Ave-Suite 12, Pittsfield MA 1201', '1201 Pittsfield MA 12, 555 Hubbard Ave-Suite'),
                ('300 Colony Place, Plymouth MA 2360', 'Place, MA 300 Plymouth 2360 Colony'),
                ('301 Falls Blvd, Quincy MA 2169', '301 Quincy Blvd, MA 2169 Falls'),
                ('36 Paramount Drive, Raynham MA 2767', 'Drive, 2767 36 Paramount Raynham MA'),
                ('450 Highland Ave, Salem MA 1970', 'Salem MA 1970 Highland Ave, 450'),
                ('1180 Fall River Avenue, Seekonk MA 2771', 'MA Fall River Avenue, 2771 1180 Seekonk'),
                ('1105 Boston Road, Springfield MA 1119', '1119 Road, Boston Springfield MA 1105'),
                ('100 Charlton Road, Sturbridge MA 1566', '100 Charlton Sturbridge Road, 1566 MA'),
                ('262 Swansea Mall Dr, Swansea MA 2777', 'Dr, Mall 2777 Swansea 262 Swansea MA'),
                ('333 Main Street, Tewksbury MA 1876', 'MA Street, 1876 Tewksbury Main 333'),
                ('550 Providence Hwy, Walpole MA 2081', 'Walpole 2081 Providence MA 550 Hwy,'),
                ('352 Palmer Road, Ware MA 1082', 'Palmer Road, 352 Ware 1082 MA'),
                ('3005 Cranberry Hwy Rt 6 28, Wareham MA 2538', 'Rt Wareha Cranberry 2538 MA 28, 3005 6 Hwy'),
                ('250 Rt 59, Airmont NY 10901', '59, Airmont 250 10901 NY Rt'),
                ('141 Washington Ave Extension, Albany NY 12205', 'Washington NY 12205 141 Albany Ave Extension,'),
                ('13858 Rt 31 W, Albion NY 14411', 'Albion Rt 14411 W, 13858 NY 31'),
                ('2055 Niagara Falls Blvd, Amherst NY 14228', 'Niagara Amherst 14228 NY Blvd, Falls 2055'), (
                    '101 Sanford Farm Shpg Center, Amsterdam NY 12010',
                    'Shpg Farm Sanford 101 Center, Amsterdam NY 12010'),
                ('297 Grant Avenue, Auburn NY 13021', 'Grant NY Auburn 13021 297 Avenue,'),
                ('4133 Veterans Memorial Drive, Batavia NY 14020', 'Batavia NY Drive, Memorial Veterans 4133 14020'), (
                    '6265 Brockport Spencerport Rd, Brockport NY 14420',
                    '6265 Brockport 14420 Brockport Spencerport NY Rd,'),
                ('5399 W Genesse St, Camillus NY 13031', 'Camillus 13031 NY W Genesse 5399 St,'),
                ('3191 County rd 10, Canandaigua NY 14424', 'Canandaigua 10, NY County 3191 rd 14424'),
                ('30 Catskill, Catskill NY 12414', 'NY 12414 30 Catskill Catskill,'),
                ('161 Centereach Mall, Centereach NY 11720', 'NY 11720 161 Centereach Centereach Mall,'),
                ('3018 East Ave, Central Square NY 13036', '13036 Central Square NY 3018 East Ave,'),
                ('100 Thruway Plaza, Cheektowaga NY 14225', 'Plaza, Thruway 14225 Cheektowaga 100 NY'),
                ('8064 Brewerton Rd, Cicero NY 13039', 'Brewerton Cicero 8064 NY Rd, 13039'),
                ('5033 Transit Road, Clarence NY 14031', 'Clarence Transit 5033 14031 NY Road,'),
                ('3949 Route 31, Clay NY 13041', 'NY Clay Route 13041 3949 31,'),
                ('139 Merchant Place, Cobleskill NY 12043', 'Merchant 139 NY Cobleskill 12043 Place,'),
                ('85 Crooked Hill Road, Commack NY 11725', 'Road, 85 Hill 11725 Crooked Commack NY'),
                ('872 Route 13, Cortlandville NY 13045', '13045 13, NY Cortlandville Route 872'),
                ('279 Troy Road, East Greenbush NY 12061', 'NY Troy 12061 East 279 Road, Greenbush'),
                ('2465 Hempstead Turnpike, East Meadow NY 11554', 'East Hempstead Meadow 2465 NY 11554 Turnpike,'),
                ('6438 Basile Rowe, East Syracuse NY 13057', 'Syracuse 13057 NY Basile East Rowe, 6438'),
                ('25737 US Rt 11, Evans Mills NY 13637', '25737 13637 Evans Mills Rt US NY 11,'),
                ('901 Route 110, Farmingdale NY 11735', '110, Farmingdale 11735 901 NY Route'),
                ('2400 Route 9, Fishkill NY 12524', 'Route 2400 NY Fishkill 12524 9,'),
                ('10401 Bennett Road, Fredonia NY 14063', 'NY Fredoni Bennett Road, 1041 14063'),
                ('1818 State Route 3, Fulton NY 13069', 'NY 13069 Rout State 3, Fluton 1818'),
                ('4300 Lakeville Road, Geneseo NY 14454', '4300 Road, 14454 Geneseo NY Lakeville'),
                ('990 Route 5 20, Geneva NY 14456', 'NY 14456 Route 990 5 Geneva 20,'),
                ('311 RT 9W, Glenmont NY 12077', '12077 RT 311 NY 9W, Glenmont'),
                ('200 Dutch Meadows Ln, Glenville NY 12302', 'Glenville 12302 200 Dutch NY Ln, Meadows'),
                ('100 Elm Ridge Center Dr, Greece NY 14626', 'Ridge Center Elm Greece NY 100 Dr, 14626'),
                ('1549 Rt 9, Halfmoon NY 12065', 'Halfmoon Rt 1549 9, 12065 NY'),
                ('5360 Southwestern Blvd, Hamburg NY 14075', '14075 5360 Southwestern Blvd, NY Hamburg'),
                ('103 North Caroline St, Herkimer NY 13350', 'St, NY 13350 North Herkimer Caroline 103'),
                ('1000 State Route 36, Hornell NY 14843', '14843 Hornell State NY 1000 36, Route'),
                ('1400 County Rd 64, Horseheads NY 14845', '64, 1400 NY Rd County Horseheads 14845'),
                ('135 Fairgrounds Memorial Pkwy, Ithaca NY 14850', 'Ithaca NY Memorial Pkwy, 135 Fairgrounds 14850'),
                ('2 Gannett Dr, Johnson City NY 13790', 'Johnson 2 City NY 13790 Dr, Gannett'),
                ('233 5th Ave Ext, Johnstown NY 12095', '233 Ext, 5th 12095 Ave Johnstown NY'),
                ('601 Frank Stottile Blvd, Kingston NY 12401', '12401 Kinston Blvd, NY Stottile Frank 601'),
                ('350 E Fairmount Ave, Lakewood NY 14750', 'Fairmount E NY Ave, 350 Lakewood 14750'),
                ('4975 Transit Rd, Lancaster NY 14086', '4975 Rd, Transit 14086 NY Lancaster'),
                ('579 Troy-Schenectady Road, Latham NY 12110', 'NY Road, Troy-Schenectady 579 Latham 12110'),
                ('5783 So Transit Road, Lockport NY 14094', 'Road, Lockport So NY Transit 5783 14094'),
                ('7155 State Rt 12 S, Lowville NY 13367', 'State S, 13367 7155 Rt NY Lowville 12'),
                ('425 Route 31, Macedon NY 14502', 'NY 14502 425 31, Route Macedon'),
                ('3222 State Rt 11, Malone NY 12953', '12953 Malone 11, Rt State NY 3222'),
                ('200 Sunrise Mall, Massapequa NY 11758', '200 Massapequa NY 11758 Sunrise Mall,'),
                ('43 Stephenville St, Massena NY 13662', 'NY Stephenville Massena 43 St, 13662'),
                ('750 Middle Country Road, Middle Island NY 11953', 'Middle Country 750 Island 11953 NY Middle Road,'),
                ('470 Route 211 East, Middletown NY 10940', '470 211 Middleown 10940 NY Route East,'),
                ('3133 E Main St, Mohegan Lake NY 10547', '3133 Main Mohegan NY St, E 10547 Lake'),
                ('288 Larkin, Monroe NY 10950', '288 NY Monoer 10950 Lakrin,'),
                ('41 Anawana Lake Road, Monticello NY 12701', 'Anawana Road, Monticello 41 NY Lake 12701'),
                ('4765 Commercial Drive, New Hartford NY 13413', 'Drive, Hartford 4765 New Commercial 13413 NY'),
                ('1201 Rt 300, Newburgh NY 12550', '1201 12550 Newburgh NY 300, Rt'),
                ('255 W Main St, Avon CT 6001', 'Main 6001 St, 255 CT Avon W'),
                ('120 Commercial Parkway, Branford CT 6405', 'Commercial 120 Parkway, 6405 Branford CT'),
                ('1400 Farmington Ave, Bristol CT 6010', '1400 6010 Ave, CT Farmington Bristol'),
                ('161 Berlin Road, Cromwell CT 6416', 'Cromwell 6416 Road, Berlin 161 CT'),
                ('67 Newton Rd, Danbury CT 6810', '67 6810 Danbury CT Rd, Newton'),
                ('656 New Haven Ave, Derby CT 6418', 'New 6418 Ave, Derby Haven 656 CT'),
                ('69 Prospect Hill Road, East Windsor CT 6088', 'East 6088 Windsor Road, Hill Prospect 69 CT'),
                ('150 Gold Star Hwy, Groton CT 6340', 'Groton Gold Star CT 150 6340 Hwy,'),
                ('900 Boston Post Road, Guilford CT 6437', 'Boston CT Road, 900 Guilford Post 6437'),
                ('2300 Dixwell Ave, Hamden CT 6514', 'Ave, 2300 6514 Hamden CT Dixwell'),
                ('495 Flatbush Ave, Hartford CT 6106', 'Flatbush Ave, 6106 Hartford CT 495'),
                ('180 River Rd, Lisbon CT 6351', '6351 River CT 180 Lisbon Rd,'),
                ('420 Buckland Hills Dr, Manchester CT 6040', 'Manchester 420 Dr, 6040 CT Buckland Hills'),
                ('1365 Boston Post Road, Milford CT 6460', '1365 6460 Boston Road, Milford Post CT'),
                ('1100 New Haven Road, Naugatuck CT 6770', 'Road, 1100 Haven 6770 Naugatuck CT New'),
                ('315 Foxon Blvd, New Haven CT 6513', 'Blvd, New 315 6513 Foxon Haven CT'),
                ('164 Danbury Rd, New Milford CT 6776', 'Danbury 6776 164 Rd, Milford New CT'),
                ('3164 Berlin Turnpike, Newington CT 6111', 'Turnpike, CT 3164 6111 Newington Berlin'),
                ('474 Boston Post Road, North Windham CT 6256', '474 6256 Post North CT Road, Boston Windham'),
                ('650 Main Ave, Norwalk CT 6851', 'arNowkl Main CT Avenue, 650 6851'),
                ('680 Connecticut Avenue, Norwalk CT 6854', '6854 Connecticut 680 Norwalk CT Avenue,'),
                ('220 Salem Turnpike, Norwich CT 6360', '220 Norwich Salem Turnpike, CT 6360'),
                ('655 Boston Post Rd, Old Saybrook CT 6475', 'Old Rd, CT 655 Post Saybrook 6475 Boston'),
                ('625 School Street, Putnam CT 6260', 'School CT 6260 625 Street, Putnam'),
                ('80 Town Line Rd, Rocky Hill CT 6067', 'CT Hill Rd, Town Line 6067 Rocky 80'),
                ('465 Bridgeport Avenue, Shelton CT 6484', 'Bridgeport Shelton 465 6484 CT Avenue,'),
                ('235 Queen St, Southington CT 6489', 'Southington Queen 235 6489 CT St,'),
                ('150 Barnum Avenue Cutoff, Stratford CT 6614', 'Barnum tratfords Cutoff, CT 6614 150 Avenue'),
                ('970 Torringford Street, Torrington CT 6790', '6790 Street, Torrington 970 Torringford CT'),
                ('844 No Colony Road, Wallingford CT 6492', 'Colony 6492 No Wallingford 844 CT Road,'),
                ('910 Wolcott St, Waterbury CT 6705', 'Wolcott St, 910 6705 Waterbury CT'),
                ('155 Waterford Parkway No, Waterford CT 6385', 'Waterford CT 6385 No, 155 Parkway Waterford'),
                ('515 Sawmill Road, West Haven CT 6516', 'Ave, Sawmill 1608 36340 W AL Haven'),
                ('2473 Hackworth Road, Adamsville AL 35005', 'AL 35005 Adamsville 2473 Road, Hackworth'),
                ('630 Coonial Promenade Pkwy, Alabaster AL 35007', '35007 Pkwy, Alabaster 630 AL Promenade Coonial'),
                ('2643 Hwy 280 West, Alexander City AL 35010', 'Alexander West, City 280 2643 AL 35010 Hwy'),
                ('540 West Bypass, Andalusia AL 36420', '36420 Bypass, Andalusia West 540 AL'),
                ('5560 Mcclellan Blvd, Anniston AL 36206', 'Blvd, AL 5560 Anniston 36206 Mcclellan'),
                ('1450 No Brindlee Mtn Pkwy, Arab AL 35016', 'Arab Mtn 35016 1450 Pkwy, No Brindlee AL'),
                ('1011 US Hwy 72 East, Athens AL 35611', 'AL 35611 Hwy Athens 72 US East, 1011'),
                ('973 Gilbert Ferry Road Se, Attalla AL 35954', '35954 Attalla AL Se, Ferry 973 Gilbert Road'),
                ('1717 South College Street, Auburn AL 36830', '1717 AL Street, Auburn South 36830 College'),
                ('701 Mcmeans Ave, Bay Minette AL 36507', 'Bay 701 Ave, Mcmeans 36507 AL Minette'),
                ('750 Academy Drive, Bessemer AL 35022', 'Drive, Bessemer Aademy 750 35022 AL'),
                ('312 Palisades Blvd, Birmingham AL 35209', 'Birmingham AL 312 Palisades 35209 Blvd,'),
                ('1600 Montclair Rd, Birmingham AL 35210', 'AL Road, Montcair 1600 35210 Birmingham'), (
                    '5919 Trussville Crossings Pkwy, Birmingham AL 35235',
                    '5919 Pkwy, Trussville 35235 AL Crossings Birmingham'),
                ('9248 Parkway East, Birmingham AL 35206', 'Parkway East, Birmingham 9248 35206 AL'),
                ('1972 Hwy 431, Boaz AL 35957', 'Hwy 431, 1972 Boaz 35957 AL'),
                ('10675 Hwy 5, Brent AL 35034', 'Brent 35034 10675 AL 5, Hwy'),
                ('2041 Douglas Avenue, Brewton AL 36426', 'Avenue, 2041 36426 Brewton AL Douglas'),
                ('5100 Hwy 31, Calera AL 35040', '5100 AL Calera 35040 Hwy 31,'),
                ('1916 Center Point Rd, Center Point AL 35215', 'Point AL Point Rd, Center 1916 Center 35215'),
                ('1950 W Main St, Centre AL 35960', 'Centre Main 1950 35960 W St, AL'),
                ('16077 Highway 280, Chelsea AL 35043', '280, AL Highway 16077 35043 Chelsea'),
                ('1415 7Th Street South, Clanton AL 35045', '1415 7Th South, AL Clanton Street 35045'),
                ('626 Olive Street Sw, Cullman AL 35055', 'Olive Sw, Street 35055 626 Cullman AL'),
                ('27520 Hwy 98, Daphne AL 36526', '27520 Daphne 98, Hwy 36526 AL'),
                ('2800 Spring Avn SW, Decatur AL 35603', '35603 2800 Spring SW, AL Avn Decatur'),
                ('969 Us Hwy 80 West, Demopolis AL 36732', 'AL Demopolis 969 36732 Hwy West, 80 Us'),
                ('3300 South Oates Street, Dothan AL 36301', 'South Street, AL Oates 36301 Dothan 3300'),
                ('4310 Montgomery Hwy, Dothan AL 36303', '4310 Montgomery 36303 Hwy, AL Dothan'),
                ('600 Boll Weevil Circle, Enterprise AL 36330', 'AL 36330 Boll Weevil 600 Circle, Enterprise'),
                ('3176 South Eufaula Avenue, Eufaula AL 36027', 'South 3176 Avenue, AL Eufaula 36027 Eufaula'),
                ('7100 Aaron Aronov Drive, Fairfield AL 35064', 'Aronov Aaron 7100 Drive, Fairfield AL 35064'),
                ('10040 County Road 48, Fairhope AL 36533', '48, 10040 AL Road County 36533 Fairhope'),
                ('3186 Hwy 171 North, Fayette AL 35555', '171 North, Hwy 35555 Fayette 3186 AL'),
                ('3100 Hough Rd, Florence AL 35630', 'Hough 35630 AL Florence Rd, 3100'),
                ('2200 South Mckenzie St, Foley AL 36535', 'Mckenzie South AL 36535 Foley St, 2200'),
                ('2001 Glenn Bldv Sw, Fort Payne AL 35968', '2001 Bldv 35968 Glenn Fort AL Payne Sw,'),
                ('340 East Meighan Blvd, Gadsden AL 35903', 'Blvd, AL 340 35903 East Meighan Gadsden'),
                ('890 Odum Road, Gardendale AL 35071', '890 Odum Road, 35071 Gardendale AL'),
                ('1608 W Magnolia Ave, Geneva AL 36340', 'Ave, Magnolia 1608 36340 W AL Geneva'),
                ('501 Willow Lane, Greenville AL 36037', '36037 Greenville Lane, 501 AL Willow'),
                ('170 Fort Morgan Road, Gulf Shores AL 36542', '36542 Shores Road, 170 Gulf AL Fort Morgan'),
                ('11697 US Hwy 431, Guntersville AL 35976', 'Guntersville AL Hwy 11697 431, 35976 US'),
                ('42417 Hwy 195, Haleyville AL 35565', 'Haleyville 35565 42417 195, Hwy AL'),
                ('1706 Military Street South, Hamilton AL 35570', 'Street South, AL 35570 1706 Military Hamilton'),
                ('1201 Hwy 31 NW, Hartselle AL 35640', '1201 Hartselle 35640 AL Hwy 31 NW,'),
                ('209 Lakeshore Parkway, Homewood AL 35209', '35209 Parkway, AL 209 Homewood Lakeshore'),
                ('2780 John Hawkins Pkwy, Hoover AL 35244', 'John Hoover 35244 AL 2780 Pkwy, Hawkins'),
                ('5335 Hwy 280 South, Hoover AL 35242', 'Hoover 35242 280 South, Hwy 5335 AL'),
                ('1007 Red Farmer Drive, Hueytown AL 35023', 'Farmer 35023 Hueytown Red 1007 Drive, AL'),
                ('2900 S Mem PkwyDrake Ave, Huntsville AL 35801', 'Huntsville Ave, 2900 Mem PkwyDrake AL S 35801'),
                ('11610 Memorial Pkwy South, Huntsville AL 35803', 'Memorial 11610 35803 Huntsville Pkwy AL South,'),
                ('2200 Sparkman Drive, Huntsville AL 35810', 'AL Sparkman Huntsville 35810 2200 Drive,'),
                ('330 Sutton Rd, Huntsville AL 35763', '330 35763 Rd, AL Sutton Huntsville'),
                ('6140A Univ Drive, Huntsville AL 35806', 'Univ 6140A Drive, 35806 Huntsville AL'),
                ('4206 N College Ave, Jackson AL 36545', 'College N Jackson 36545 Ave, AL 4206'),
                ('1625 Pelham South, Jacksonville AL 36265', '1625 Jacksonville South, AL 36265 Pelham'),
                ('1801 Hwy 78 East, Jasper AL 35501', 'Semmes Moffett AL 7855 Rd, 36575'),
                ('8551 Whitfield Ave, Leeds AL 35094', 'Leeds Whitfield Ave, AL 35094 8551'),
                ('8650 Madison Blvd, Madison AL 35758', 'AL Madison 35758 Blvd, 8650 Madison'),
                ('145 Kelley Blvd, Millbrook AL 36054', 'Blvd, 36054 Kelley 145 AL Millbrook'),
                ('1970 S University Blvd, Mobile AL 36609', 'Mobile 36609 Blv, University 1970 AL S'),
                ('6350 Cottage Hill Road, Mobile AL 36609', 'AL Hill Mobile Cottage Road, 6350 36609'),
                ('101 South Beltline Highway, Mobile AL 36606', '101 Highway, 36606 Beltline AL South Mobile'),
                ('2500 Dawes Road, Mobile AL 36695', '36695 Mobile 2500 AL Road, Dawes'),
                ('5245 Rangeline Service Rd, Mobile AL 36619', 'AL Mobile 36619 5245 Rangeline Rd, Service'),
                ('685 Schillinger Rd, Mobile AL 36695', 'Mobile AL Schillinger 36695 Rd, 685'),
                ('3371 S Alabama Ave, Monroeville AL 36460', 'Alabama S Monroeville AL 36460 3371 Ave,'),
                ('10710 Chantilly Pkwy, Montgomery AL 36117', 'AL 36117 Chantilly Montgomery 10710 Pkwy,'),
                ('3801 Eastern Blvd, Montgomery AL 36116', 'Blvd, Eastern AL 36116 3801 Montgomery'),
                ('6495 Atlanta Hwy, Montgomery AL 36117', '6495 Montgomery AL Hwy, 36117 Atlanta'),
                ('851 Ann St, Montgomery AL 36107', 'AL St, 851 Montgomery 36107 Ann'),
                ('15445 Highway 24, Moulton AL 35650', '15445 Moulton 24, Highway 35650 AL'),
                ('517 West Avalon Ave, Muscle Shoals AL 35661', 'West 517 Ave, Shoals AL 35661 Avalon Muscle'),
                ('5710 Mcfarland Blvd, Northport AL 35476', '5710 Mcfarland Blvd, Northport 35476 AL'), (
                    '2453 2Nd Avenue East, Oneonta AL 35121  205-625-647',
                    'East, 2453 35121 2Nd Oneonta AL Avenue 205-625-647'),
                ('2900 Pepperrell Pkwy, Opelika AL 36801', 'AL Pkwy, 36801 Opelika Pepperrell 2900'),
                ('92 Plaza Lane, Oxford AL 36203', '92 36203 Plaza Lane, AL Oxford'),
                ('1537 Hwy 231 South, Ozark AL 36360', '36360 South, AL 231 Hwy 1537 Ozark'),
                ('2181 Pelham Pkwy, Pelham AL 35124', 'Pelham 218 Pkwy, 35124 Pelham AL'),
                ('165 Vaughan Ln, Pell City AL 35125', 'Pell AL Vaughan Ln, 35125 165 City'),
                ('3700 Hwy 280-431 N, Phenix City AL 36867', 'City Hwy N, 280-431 AL 36867 3700 Phenix'),
                ('1903 Cobbs Ford Rd, Prattville AL 36066', 'Rd, AL 36066 Prattville 1903 Cobbs Ford'),
                ('4180 Us Hwy 431, Roanoke AL 36274', '4180 431, Roanoke AL Hwy Us 36274'),
                ('13675 Hwy 43, Russellville AL 35653', 'AL 13675 43, 35653 Hwy Russellville'),
                ('1095 Industrial Pkwy, Saraland AL 36571', 'AL 36571 1095 Saraland Industrial Pkwy,'),
                ('24833 Johnt Reidprkw, Scottsboro AL 35768', 'Johnt Scottsboro Reidprkw, 24833 35768 AL'),
                ('1501 Hwy 14 East, Selma AL 36703', 'Hwy 1501 East, AL Selma 36703 14'),
                ('7855 Moffett Rd, Semmes AL 36575', 'Semmes Moffett AL 7855 Rd, 36575'), (
                    '150 Springville Station Blvd, Springville AL 35146',
                    'AL 35146 150 Springville Station Springville Blvd,'),
                ('690 Hwy 78, Sumiton AL 35148', 'Hough 35630 AL Florence Rd, 3100'),
                ('41301 US Hwy 280, Sylacauga AL 35150', 'Hwy 41301 US AL 35150 280, Sylacauga'),
                ('214 Haynes Street, Talladega AL 35160', 'Talladeg AL Haynes Street, 214 35160'),
                ('1300 Gilmer Ave, Tallassee AL 36078', 'Ave, AL Tallassee Gilmer 1300 36078'),
                ('34301 Hwy 43, Thomasville AL 36784', 'AL 34301 Thomasville 43, 36784 Hwy'),
                ('1420 Us 231 South, Troy AL 36081', '231 1420 36081 AL Us Troy South,'),
                ('1501 Skyland Blvd E, Tuscaloosa AL 35405', '35405 E, Tuscaloosa 1501 Bdvl Skylan'),
                ('3501 20th Av, Valley AL 36854', '20th Av, 3501 Valley 36854 AL'), (
                    '1300 Montgomery Highway, Vestavia Hills AL 35216',
                    '1300 35216 Montgomery Hills AL Highway, Vestavia'),
                ('4538 Us Hwy 231, Wetumpka AL 36092', 'AL 231, 36092 Hwy Us 4538 Wetumpka'),
                ('2575 Us Hwy 43, Winfield AL 35594', 'AL Us Winfield /2575 -35594 Hwy 43,'),
                ('Mayo Clinic 200 First Street SW Rochester MN  USA 55905',
                 'Mayo Clinic Rochester 200 First Street SW Rochester, MN 55905')]


def extract(_Str):
    return re.findall("[+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", _Str), re.findall("[a-zA-Z]+", _Str)


def find_diff(_str1, _str2):
    return list(set([x for x in _str1 + _str2 if x not in _str1 or x not in _str2]))


def get_Sorted_str(_str):
    return ''.join(sorted(''.join(e for e in _str.lower() if e.isalnum())))


def get_apha_num(_str):
    return " ".join(re.findall("[0-9a-zA-Z]+", _str))


def get_match_score(num_diff, char_diff, str1_num, Str1_char, str2_num, Str2_char):
    num_diff_dict = dict()
    char_diff_dict = dict()

    if num_diff:
        for each_num in num_diff:
            if each_num not in str1_num:
                high = process.extract(each_num, str1_num)[:2]
            elif each_num not in str2_num:
                high = process.extract(each_num, str2_num)[:2]
            num_diff_dict.update({each_num: high})
    if char_diff:
        for each_token in char_diff:
            if each_token not in Str1_char:
                high = process.extract(each_token, Str1_char)[:2]
            elif each_token not in Str2_char:
                high = process.extract(each_token, Str2_char)[:2]
            char_diff_dict.update({each_token: high})

    return num_diff_dict, char_diff_dict


def compare_address(Str1, Str2, Threshold=90):
    # _Str1 = get_Sorted_str(Str1)
    _Str1 = get_apha_num(Str1)
    # _Str2 = get_Sorted_str(Str2)
    _Str2 = get_apha_num(Str2)
    # _Ratio = fuzz.ratio(_Str1.lower(), _Str2.lower())
    _Ratio = fuzz.ratio(_Str1.lower(), _Str2.lower())
    print("_Ratio", _Ratio)
    Ratio = fuzz.token_set_ratio(Str1.lower(), Str2.lower())
    print('token_set__Ratio', Ratio)
    print("Ratio", Ratio)
    default_dict = {"String1": Str1, "String2": Str2, "ratio": Ratio, "Match": "not match", "reason": ""}

    if Ratio < Threshold:
        default_dict.update({"reason": "threshold not met"})
        return default_dict
    else:
        default_dict.update({"Match": "matched"})

    str1_num, Str1_char = extract(Str1)
    str2_num, Str2_char = extract(Str2)

    num_diff = find_diff(str1_num, str2_num)
    char_diff = find_diff(Str1_char, Str2_char)

    if num_diff or char_diff:
        print("num_diff", num_diff)
        print("chardiff", char_diff)
        num_diff_dict, char_diff_dict = get_match_score(num_diff, char_diff, str1_num, Str1_char, str2_num, Str2_char)
        if num_diff and char_diff:
            default_dict.update({"reason": "number and  character diff", "num_diff": num_diff, "char_diff": char_diff,
                                 "num_diff_high_match": num_diff_dict, "char_diff_high_match": char_diff_dict})
        elif num_diff and not char_diff:
            default_dict.update({"reason": "number diff", "num_diff": num_diff, "num_diff_high_match": num_diff_dict})

        elif char_diff and not num_diff:
            default_dict.update(
                {"reason": "character diff", "char_diff": char_diff, "char_diff_high_match": char_diff_dict})

    return default_dict


# print(compare_address("Mary Crowley Cancer Research 7776 -medicalCity Forest Lane, Building 707",
#                       'Mary rowlecy Cancer Research 7777 Forest Lane, Building 707'))

compare_dict_list = []
for each in address_list:
    dict_ = compare_address(*each)
    compare_dict_list.append(dict_)

import pandas as pd

df = pd.DataFrame(compare_dict_list)
df.to_csv("compare_address.csv")
print("Done")
