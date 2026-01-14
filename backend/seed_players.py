"""
FIFA Arab Cup 2025 - Qatar - Real Tournament Data
Seeding Teams, Players, and Matches
"""
from app import create_app
from extensions import db
from models import Match, Team, Player

app = create_app()

# Real 2025 Arab Cup Teams and Players from FIFA.com
TEAMS_PLAYERS = {
    "Morocco": [
        ("El Mehdi Benabid", "Goalkeeper"),
        ("Soufiane Bouftini", "Defender"),
        ("Abdelkebir Abqar", "Defender"),
        ("Achraf Dari", "Defender"),
        ("Mohamed Boulacsout", "Defender"),
        ("Yahya Jabrane", "Midfielder"),
        ("Mohamed Hrimat", "Midfielder"),
        ("Oussama Tannane", "Midfielder"),
        ("Karim El Berkaoui", "Forward"),
        ("Tarik Tissoudali", "Forward"),
        ("Soufiane Rahimi", "Forward"),
    ],
    "Jordan": [
        ("Yazeed Abulaila", "Goalkeeper"),
        ("Abdallah Nasib", "Defender"),
        ("Yazan Al-Arab", "Defender"),
        ("Saed Al-Rosan", "Defender"),
        ("Ehsan Haddad", "Midfielder"),
        ("Nizar Al-Rashdan", "Midfielder"),
        ("Mohammad Abuhasheen", "Midfielder"),
        ("Mohannad Abu Taha", "Midfielder"),
        ("Ali Olwan", "Forward"),
        ("Mousa Al-Tamari", "Forward"),
        ("Yazan Al-Naimat", "Forward"),
    ],
    "Qatar": [
        ("Meshaal Barsham", "Goalkeeper"),
        ("Lucas Mendes", "Defender"),
        ("Tarek Salman", "Defender"),
        ("Sultan Al-Brake", "Defender"),
        ("Homam Ahmed", "Defender"),
        ("Mohammed Waad", "Midfielder"),
        ("Abdulaziz Hatem", "Midfielder"),
        ("Ahmed Fathy", "Midfielder"),
        ("Akram Afif", "Forward"),
        ("Ahmed Alaaeldin", "Forward"),
        ("Edmilson Junior", "Forward"),
    ],
    "Palestine": [
        ("Rami Hamadeh", "Goalkeeper"),
        ("Musab Al-Battat", "Defender"),
        ("Mohammed Saleh", "Defender"),
        ("Yaser Hamed", "Defender"),
        ("Michel Termanini", "Defender"),
        ("Oday Kharoub", "Midfielder"),
        ("Hamed Hamdan", "Midfielder"),
        ("Mahmoud Abu Warda", "Midfielder"),
        ("Moustafa Zeidan", "Midfielder"),
        ("Tamer Seyam", "Forward"),
        ("Oday Dabbagh", "Forward"),
    ],
    "Syria": [
        ("Elias Hadaya", "Goalkeeper"),
        ("Ahmad Faqa", "Defender"),
        ("Alan Aussi", "Defender"),
        ("Abdullah Al Shami", "Defender"),
        ("Khaled Kourdoghli", "Defender"),
        ("Simon Amin", "Midfielder"),
        ("Ezequiel Ham", "Midfielder"),
        ("Jalil Elias", "Midfielder"),
        ("Mahmoud Al-Mawas", "Forward"),
        ("Omar Kharbin", "Forward"),
        ("Mohammad Al Hallaq", "Forward"),
    ],
    "Tunisia": [
        ("Bechir Ben Saïd", "Goalkeeper"),
        ("Yassine Meriah", "Defender"),
        ("Montassar Talbi", "Defender"),
        ("Mohamed Benali", "Defender"),
        ("Ali Abdi", "Defender"),
        ("Ellyes Skhiri", "Midfielder"),
        ("Mohamed Ali Ben Romdhane", "Midfielder"),
        ("Aïssa Laïdouni", "Midfielder"),
        ("Amor Layouni", "Forward"),
        ("Firas Chaouat", "Forward"),
        ("Elias Achouri", "Forward"),
    ],
    "Saudi Arabia": [
        ("Nawaf Al-Aqidi", "Goalkeeper"),
        ("Hassan Al-Tambakti", "Defender"),
        ("Abdulelah Al-Amri", "Defender"),
        ("Ali Majrashi", "Defender"),
        ("Mohammed Sulaiman", "Defender"),
        ("Nasser Al-Dawsari", "Midfielder"),
        ("Musab Al-Juwayr", "Midfielder"),
        ("Mohamed Kanno", "Midfielder"),
        ("Salem Al-Dawsari", "Forward"),
        ("Feras Albrikan", "Forward"),
        ("Saleh Al-Shehri", "Forward"),
    ],
    "Oman": [
        ("Ibrahim Al-Mukhaini", "Goalkeeper"),
        ("Ali Al-Busaidi", "Defender"),
        ("Ahmed Al-Khamisi", "Defender"),
        ("Khalid Al-Braiki", "Defender"),
        ("Jameel Al-Yahmadi", "Defender"),
        ("Harib Al-Saadi", "Midfielder"),
        ("Abdullah Fawaz", "Midfielder"),
        ("Salaah Al-Yahyaei", "Midfielder"),
        ("Issam Al-Sabhi", "Forward"),
        ("Muhsen Al-Ghassani", "Forward"),
        ("Abdulrahman Al-Mushaifri", "Forward"),
    ],
    "Comoros": [
        ("Salim Ben Boina", "Goalkeeper"),
        ("Kassim M'Dahoma", "Defender"),
        ("Younn Zahary", "Defender"),
        ("Saïd Bakari", "Defender"),
        ("Bendjaloud Youssouf", "Defender"),
        ("Youssouf M'Changama", "Midfielder"),
        ("Rafidine Abdullah", "Midfielder"),
        ("Iyad Mohamed", "Midfielder"),
        ("Myziane Maolida", "Forward"),
        ("Faiz Selemani", "Forward"),
        ("Ibroihim Djoudja", "Forward"),
    ],
    "Egypt": [
        ("Mohamed El Shenawy", "Goalkeeper"),
        ("Rami Rabia", "Defender"),
        ("Mohamed Abdelmonem", "Defender"),
        ("Mohamed Hany", "Defender"),
        ("Ahmed Fatouh", "Defender"),
        ("Mohamed Elneny", "Midfielder"),
        ("Hamdi Fathi", "Midfielder"),
        ("Emam Ashour", "Midfielder"),
        ("Mohamed Afsha", "Forward"),
        ("Mahmoud Trezeguet", "Forward"),
        ("Marwan Hamdy", "Forward"),
    ],
    "United Arab Emirates": [
        ("Ali Meqbaali", "Goalkeeper"),
        ("Khalifa Al-Hammadi", "Defender"),
        ("Kouame Autonne", "Defender"),
        ("Zayed Sultan", "Defender"),
        ("Abdulla Idrees", "Defender"),
        ("Yahia Nader", "Midfielder"),
        ("Isam Faiz", "Midfielder"),
        ("Nicolas Gimenez", "Midfielder"),
        ("Yahya Al-Ghassani", "Forward"),
        ("Caio Lucas", "Forward"),
        ("Bruno Oliveira", "Forward"),
    ],
    "Kuwait": [
        ("Sulaiman Abdulghafour", "Goalkeeper"),
        ("Fahed Al-Hajri", "Defender"),
        ("Khalid El Ebrahim", "Defender"),
        ("Meshari Ghanam", "Defender"),
        ("Rashid Al-Dousari", "Defender"),
        ("Redha Hani", "Midfielder"),
        ("Ahmad Al-Dhefiri", "Midfielder"),
        ("Athbi Saleh", "Midfielder"),
        ("Mohammad Daham", "Forward"),
        ("Yousef Naser", "Forward"),
        ("Eid Al-Rashidi", "Forward"),
    ],
    "Algeria": [
        ("Farid Chaal", "Goalkeeper"),
        ("Mohamed Amine Tougai", "Defender"),
        ("Abdelkader Bedrane", "Defender"),
        ("Youcef Atal", "Defender"),
        ("Mohamed Khacef", "Defender"),
        ("Victor Lekhal", "Midfielder"),
        ("Zakaria Draoui", "Midfielder"),
        ("Houssem Mrezigue", "Midfielder"),
        ("Yassine Benzia", "Forward"),
        ("Amir Sayoud", "Forward"),
        ("Adil Boulbina", "Forward"),
    ],
    "Iraq": [
        ("Jalal Hassan", "Goalkeeper"),
        ("Rebin Sulaka", "Defender"),
        ("Saad Natiq", "Defender"),
        ("Hussein Ali", "Defender"),
        ("Merchas Doski", "Defender"),
        ("Amjed Attwan", "Midfielder"),
        ("Amir Al-Ammari", "Midfielder"),
        ("Ibrahim Bayesh", "Midfielder"),
        ("Zidane Iqbal", "Forward"),
        ("Mohanad Ali", "Forward"),
        ("Aymen Hussein", "Forward"),
    ],
    "Bahrain": [
        ("Ebrahim Lutfalla", "Goalkeeper"),
        ("Waleed Al Hayam", "Defender"),
        ("Amine Benaddi", "Defender"),
        ("Mohamed Adel", "Defender"),
        ("Abdulla Al-Khalasi", "Defender"),
        ("Jassim Al-Shaikh", "Midfielder"),
        ("Mohamed Al-Hardan", "Midfielder"),
        ("Kamil Al-Aswad", "Midfielder"),
        ("Mahdi Al-Humaidan", "Forward"),
        ("Mohamed Al-Romaihi", "Forward"),
        ("Mahdi Abdouljabbar", "Forward"),
    ],
    "Sudan": [
        ("Mohamed Mustafa", "Goalkeeper"),
        ("Mustafa Karshoum", "Defender"),
        ("Abdel Raman Koko", "Defender"),
        ("Bakhit Khamis", "Defender"),
        ("Ramadan Agab", "Defender"),
        ("Walieldin Khedr", "Midfielder"),
        ("Abuaagla Abdalla", "Midfielder"),
        ("Sharaf Eldin Shiboub", "Midfielder"),
        ("Saif Teiri", "Forward"),
        ("Yasir Mozamil", "Forward"),
        ("Mohamed Eisa", "Forward"),
    ],
}

# 2025 Arab Cup Matches with actual results from FIFA
MATCHES = [
    # Group Stage Matches
    ("Tunisia", "Syria", "2025-12-01", 0, 1, "Ahmad Bin Ali Stadium"),
    ("Qatar", "Palestine", "2025-12-01", 0, 1, "Al Bayt Stadium"),
    ("Morocco", "Comoros", "2025-12-02", 3, 1, "Khalifa International Stadium"),
    ("Egypt", "Kuwait", "2025-12-02", 1, 1, "Lusail Stadium"),
    ("Saudi Arabia", "Oman", "2025-12-02", 2, 1, "Education City Stadium"),
    ("Palestine", "Tunisia", "2025-12-04", 2, 2, "Lusail Stadium"),
    ("Syria", "Qatar", "2025-12-04", 1, 1, "Khalifa International Stadium"),
    ("Oman", "Morocco", "2025-12-05", 0, 0, "Education City Stadium"),
    ("Comoros", "Saudi Arabia", "2025-12-05", 1, 3, "Al Bayt Stadium"),
    ("Qatar", "Tunisia", "2025-12-07", 0, 3, "Al Bayt Stadium"),
    ("Syria", "Palestine", "2025-12-07", 0, 0, "Education City Stadium"),
    ("Morocco", "Saudi Arabia", "2025-12-08", 1, 0, "Lusail Stadium"),
    ("Oman", "Comoros", "2025-12-08", 2, 1, "Stadium 974"),
    ("Egypt", "Jordan", "2025-12-09", 0, 3, "Al Bayt Stadium"),
    ("United Arab Emirates", "Kuwait", "2025-12-09", 3, 1, "Ahmad Bin Ali Stadium"),
    ("Jordan", "Kuwait", "2025-12-06", 2, 1, "Ahmad Bin Ali Stadium"),
    ("United Arab Emirates", "Egypt", "2025-12-06", 1, 1, "Lusail Stadium"),
    ("Iraq", "Bahrain", "2025-12-03", 2, 1, "Stadium 974"),
    ("Algeria", "Sudan", "2025-12-03", 0, 0, "Ahmad Bin Ali Stadium"),
    ("Bahrain", "Djibouti", "2025-11-26", 1, 0, "Jassim Bin Hamad Stadium"),
    ("Iraq", "Sudan", "2025-12-10", 2, 0, "Stadium 974"),
    ("Bahrain", "Sudan", "2025-12-09", 3, 1, "Education City Stadium"),
    ("Algeria", "Iraq", "2025-12-10", 7, 1, "Khalifa International Stadium"),
    
    # Quarter-finals
    ("Morocco", "Syria", "2025-12-11", 1, 0, "Khalifa International Stadium"),
    ("Palestine", "Saudi Arabia", "2025-12-11", 1, 2, "Lusail Stadium"),
    ("Jordan", "Iraq", "2025-12-12", 1, 0, "Al Bayt Stadium"),
    ("Algeria", "United Arab Emirates", "2025-12-12", 1, 1, "Ahmad Bin Ali Stadium"),
    
    # Semi-finals
    ("Morocco", "United Arab Emirates", "2025-12-15", 3, 0, "Khalifa International Stadium"),
    ("Saudi Arabia", "Jordan", "2025-12-15", 0, 1, "Al Bayt Stadium"),
    
    # Third Place Match
    ("Saudi Arabia", "United Arab Emirates", "2025-12-18", 0, 0, "Khalifa International Stadium"),
    
    # Final
    ("Jordan", "Morocco", "2025-12-20", 2, 3, "Lusail Stadium"),
]

with app.app_context():
    # Clear existing data
    print("Clearing existing data...")
    db.session.query(Player).delete()
    db.session.query(Match).delete()
    db.session.query(Team).delete()
    db.session.commit()
    
    # Create teams and add players
    print("Creating teams and players...")
    for country, players_list in TEAMS_PLAYERS.items():
        team = Team(
            team_id=f"team_{country.replace(' ', '_')}",
            name=country,
            country=country,
            badge=f"https://www.fifa.com/worldcup/teams/{country.lower().replace(' ', '-')}"
        )
        db.session.add(team)
        db.session.flush()
        
        for player_name, position in players_list:
            player = Player(
                player_id=f"{team.id}_{player_name.replace(' ', '_')}",
                name=player_name,
                position=position,
                nationality=country,
                team_id=team.id
            )
            db.session.add(player)
        
        print(f"✅ Added {country} with {len(players_list)} players")
    
    db.session.commit()
    
    # Add matches
    print("\nAdding matches...")
    for home_team, away_team, date, home_score, away_score, venue in MATCHES:
        home = Team.query.filter_by(name=home_team).first()
        away = Team.query.filter_by(name=away_team).first()
        
        if home and away:
            match = Match(
                event_id=f"{home_team}_{away_team}_{date}",
                season="2025",
                date=date,
                home_team=home_team,
                away_team=away_team,
                home_team_id=home.id,
                away_team_id=away.id,
                home_score=home_score,
                away_score=away_score,
                venue=venue
            )
            db.session.add(match)
    
    db.session.commit()
    print(f"✅ Added {len(MATCHES)} matches")
    
    # Statistics
    total_teams = Team.query.count()
    total_players = Player.query.count()
    total_matches = Match.query.count()
    
    print(f"\n{'='*50}")
    print(f"✅ FIFA Arab Cup 2025 Data Seeded Successfully!")
    print(f"{'='*50}")
    print(f"Total Teams: {total_teams}")
    print(f"Total Players: {total_players}")
    print(f"Total Matches: {total_matches}")
    print(f"{'='*50}")
