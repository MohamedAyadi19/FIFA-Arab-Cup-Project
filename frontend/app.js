const apiUrl = "http://localhost:5000"; // Backend URL
window.apiUrl = apiUrl; // Make it globally accessible
let jwtToken = ""; // Store the JWT token (session only - not persisted)
// CSV data is already in database, so mark as loaded
let teamsLoaded = true;
let matchesLoaded = true;
let playersLoaded = true;

// Caches to reuse data for lineup view
let teamsCache = [];
let playersCache = [];

// Will be populated from database
let arabCupCountries = [];

// Allowed Arab Cup teams (user-provided list)
const allowedTeamNames = [
    "Bahrain National Team",
    "Syria National Team",
    "Palestine National Team",
    "Oman National Team",
    "Lebanon National Team",
    "Yemen National Team",
    "Kuwait National Team",
    "Libya National Team",
    "Comoros National Team",
    "Mauritania National Team",
    "Sudan National Team",
    "Djibouti National Team",
    "South Sudan National Team",
    "Somalia National Team",
    "Jordan National Team",
    "Saudi Arabia National Team",
    "Qatar National Team",
    "Iraq National Team",
    "United Arab Emirates National Team",
    "Algeria National Team",
    "Morocco National Team",
    "Egypt National Team",
    "Tunisia National Team",
];

// Expose allowlist and flags for other modules (statistics module uses it)
window.allowedTeamNames = allowedTeamNames;

function teamNameToCountry(name) {
    return (name || "").replace(" National Team", "").trim();
}

// ISO flag mapping for consistent flag rendering
const flagMap = {
    "Qatar": "https://flagcdn.com/w80/qa.png",
    "Tunisia": "https://flagcdn.com/w80/tn.png",
    "Syria": "https://flagcdn.com/w80/sy.png",
    "Palestine": "https://flagcdn.com/w80/ps.png",
    "Morocco": "https://flagcdn.com/w80/ma.png",
    "Saudi Arabia": "https://flagcdn.com/w80/sa.png",
    "Oman": "https://flagcdn.com/w80/om.png",
    "Comoros": "https://flagcdn.com/w80/km.png",
    "Egypt": "https://flagcdn.com/w80/eg.png",
    "Jordan": "https://flagcdn.com/w80/jo.png",
    "United Arab Emirates": "https://flagcdn.com/w80/ae.png",
    "UAE": "https://flagcdn.com/w80/ae.png",
    "Kuwait": "https://flagcdn.com/w80/kw.png",
    "Algeria": "https://flagcdn.com/w80/dz.png",
    "Iraq": "https://flagcdn.com/w80/iq.png",
    "Bahrain": "https://flagcdn.com/w80/bh.png",
    "Sudan": "https://flagcdn.com/w80/sd.png",
    "Djibouti": "https://flagcdn.com/w80/dj.png",
    "South Sudan": "https://flagcdn.com/w80/ss.png",
    "Somalia": "https://flagcdn.com/w80/so.png",
    "Yemen": "https://flagcdn.com/w80/ye.png",
    "Libya": "https://flagcdn.com/w80/ly.png",
    "Mauritania": "https://flagcdn.com/w80/mr.png",
    "Lebanon": "https://flagcdn.com/w80/lb.png"
};

// Share flag map for other modules that render player/team visuals
window.flagMap = flagMap;

const flagEmojiFallback = "🏴";

function getFlag(country) {
    return flagMap[country] || "";
}

function getPlayerCountry(player) {
    return player?.nationality || player?.["Current Club"] || player?.team || player?.country || "";
}

function getPlayerName(player) {
    return player?.full_name || player?.name || "Unknown";
}

function normalizeMatch(match) {
    let homeTeam = match.home_team_name || match.home_team || match.HomeTeam || match["Home Team"] || match.country_home || "Unknown";
    let awayTeam = match.away_team_name || match.away_team || match.AwayTeam || match["Away Team"] || match.country_away || "Unknown";
    
    // Map CSV abbreviations to full country names
    const teamAbbreviationMap = {
        "UAE": "United Arab Emirates",
        "KSA": "Saudi Arabia"
    };
    
    homeTeam = teamAbbreviationMap[homeTeam] || homeTeam;
    awayTeam = teamAbbreviationMap[awayTeam] || awayTeam;
    
    const homeScore = match.home_team_goal_count ?? match.home_score ?? match["home_score"] ?? match["Home Score"] ?? 0;
    const awayScore = match.away_team_goal_count ?? match.away_score ?? match["away_score"] ?? match["Away Score"] ?? 0;
    const date = match.date_GMT || match.date || match.match_date || match.timestamp || "";
    const venue = match.stadium_name || match.venue || "";
    const gameWeek = match['Game Week'] || match.game_week || 'N/A';
    return { homeTeam, awayTeam, homeScore, awayScore, date, venue, gameWeek };
}

// Function to display team flags and names
async function displayTeams() {
    console.log('displayTeams called');
    const response = await fetch(`${apiUrl}/api/teams/`);
    console.log('Teams response status:', response.status);
    const teams = await response.json();
    console.log('Teams data:', teams.length, 'teams loaded');

    const allowedCountries = new Set(allowedTeamNames.map(teamNameToCountry));
    const filteredTeams = teams.filter(t => allowedCountries.has(t.country) || allowedTeamNames.includes(t.team_name));

    teamsCache = filteredTeams; // cache
    const teamsContainer = document.getElementById("teamFlags");

    // Clear previous content
    teamsContainer.innerHTML = "";

    // Define tournament data for each team
    const tournamentData = {
        "Algeria": { position: "Quarter-final", group: "", topScorer: "-" },
        "Bahrain": { position: "Group D", group: "Group D", topScorer: "-" },
        "Comoros": { position: "Group B", group: "Group B", topScorer: "-" },
        "Djibouti": { position: "Play-off", group: "", topScorer: "-" },
        "Egypt": { position: "Quarter-final", group: "Group D", topScorer: "-" },
        "Iraq": { position: "Group D", group: "Group D", topScorer: "-" },
        "Jordan": { position: "Runner-up", group: "Group E", topScorer: "-" },
        "Kuwait": { position: "Group E", group: "Group E", topScorer: "-" },
        "Lebanon": { position: "Group A", group: "Group A", topScorer: "-" },
        "Libya": { position: "Play-off", group: "", topScorer: "-" },
        "Mauritania": { position: "Play-off", group: "", topScorer: "-" },
        "Morocco": { position: "Champions", group: "Group C", topScorer: "-" },
        "Oman": { position: "Group C", group: "Group C", topScorer: "-" },
        "Palestine": { position: "Group A", group: "Group A", topScorer: "-" },
        "Qatar": { position: "Semi-final", group: "Group A", topScorer: "-" },
        "Saudi Arabia": { position: "Semi-final", group: "Group C", topScorer: "-" },
        "Somalia": { position: "Play-off", group: "", topScorer: "-" },
        "South Sudan": { position: "Play-off", group: "", topScorer: "-" },
        "Sudan": { position: "Group D", group: "Group D", topScorer: "-" },
        "Syria": { position: "Group A", group: "Group A", topScorer: "-" },
        "Tunisia": { position: "Third place", group: "Group A", topScorer: "-" },
        "United Arab Emirates": { position: "Semi-final", group: "Group B", topScorer: "-" },
        "Yemen": { position: "Group B", group: "Group B", topScorer: "-" }
    };

    // Display all teams with tournament info
    filteredTeams.forEach(team => {
        const teamCard = document.createElement("div");
        teamCard.classList.add("team-card-pro");
        teamCard.dataset.country = team.country;

        const flagUrl = getFlag(team.country) || team.badge;
        const teamData = tournamentData[team.country] || { position: "Participant", group: "", topScorer: "-" };
        
        // Color classes based on achievement
        let colorClass = "team-blue";
        if (teamData.position === "Champions") colorClass = "team-gold";
        else if (teamData.position === "Runner-up") colorClass = "team-silver";
        else if (teamData.position.includes("Semi-final")) colorClass = "team-blue";
        else if (teamData.position.includes("Quarter-final")) colorClass = "team-green";
        else if (teamData.position.includes("Play-off")) colorClass = "team-light-blue";
        else if (teamData.position.includes("Group")) colorClass = "team-red";

        teamCard.innerHTML = `
            <div class="team-header ${colorClass}">
                ${flagUrl ? `<img class="team-flag-large" src="${flagUrl}" alt="${team.country}">` : flagEmojiFallback}
                <div class="team-badges">
                    ${team.badge ? `<img class="team-badge-icon" src="${team.badge}" alt="Badge">` : ''}
                </div>
            </div>
            <div class="team-content">
                <h3 class="team-name-large">${team.country}</h3>
                <div class="team-info-row">
                    <span class="info-label">Final position</span>
                    <span class="info-value">${teamData.position}</span>
                </div>
                ${teamData.group ? `<div class="team-info-row"><span class="info-label">Group</span><span class="info-value">${teamData.group}</span></div>` : ''}
                <div class="team-info-row">
                    <span class="info-label">Top goalscorer</span>
                    <span class="info-value">${teamData.topScorer}</span>
                </div>
            </div>
        `;
        
        teamCard.addEventListener('click', () => {
            // Show players section and filter by this country
            const playersSection = document.getElementById('players');
            const countryFilter = document.getElementById('playersCountryFilter');
            playersSection.style.display = 'block';
            countryFilter.value = team.country;
            displayPlayers(team.country);
            playersSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        });
        teamsContainer.appendChild(teamCard);
    });
}

// Populate the dropdown filter with countries
function populateCountryFilter() {
    const countryFilter = document.getElementById("countryFilter");
    const playersCountryFilter = document.getElementById("playersCountryFilter");
    
    // Use allowedTeamNames mapped to countries
    const countries = allowedTeamNames.map(teamNameToCountry).sort();
    
    // Populate matches country filter
    if (countryFilter) {
        countryFilter.innerHTML = "<option value=''>Display All</option>";
        countries.forEach(country => {
            const option = document.createElement("option");
            option.value = country;
            option.textContent = country;
            countryFilter.appendChild(option);
        });
    }
    
    // Populate players country filter
    if (playersCountryFilter) {
        playersCountryFilter.innerHTML = "<option value=''>Display All</option>";
        countries.forEach(country => {
            const option = document.createElement("option");
            option.value = country;
            option.textContent = country;
            playersCountryFilter.appendChild(option);
        });
    }
}

// Fetch and display all matches
async function displayMatches(country = '') {
    const response = await fetch(`${apiUrl}/api/matches/`);
    const rawMatches = await response.json();
    const matches = rawMatches.map(normalizeMatch);
    const matchesContainer = document.getElementById("allMatches");

    const allowedCountries = new Set(arabCupCountries.length ? arabCupCountries : allowedTeamNames.map(teamNameToCountry));

    const filtered = matches.filter(m => {
        const inScope = allowedCountries.has(m.homeTeam) && allowedCountries.has(m.awayTeam);
        const countryMatch = !country || m.homeTeam === country || m.awayTeam === country;
        return inScope && countryMatch;
    }).sort((a, b) => {
        // Parse CSV date format: "Nov 25 2025 - 1:00pm"
        const parseDate = (dateStr) => {
            if (!dateStr || dateStr === 'Date N/A') return new Date(0);
            // Extract just the date part before the dash
            const datePart = dateStr.split(' - ')[0];
            return new Date(datePart);
        };
        return parseDate(b.date) - parseDate(a.date);
    });

    // Group matches by date
    const matchesByDate = {};
    filtered.forEach(match => {
        // Parse and format date from CSV format
        let dateKey = 'Unknown Date';
        if (match.date && match.date !== 'Date N/A') {
            const datePart = match.date.split(' - ')[0];
            const parsedDate = new Date(datePart);
            if (!isNaN(parsedDate.getTime())) {
                dateKey = parsedDate.toISOString().split('T')[0]; // YYYY-MM-DD
            }
        }
        if (!matchesByDate[dateKey]) matchesByDate[dateKey] = [];
        matchesByDate[dateKey].push(match);
    });

    let matchHtml = '';
    Object.keys(matchesByDate).forEach(dateKey => {
        const dateObj = new Date(dateKey);
        const formattedDate = dateKey !== 'Unknown Date' ? 
            dateObj.toLocaleDateString('en-US', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }) : 
            'Unknown Date';
        
        matchHtml += `<div class="match-date-header">${formattedDate}</div>`;
        
        matchesByDate[dateKey].forEach(match => {
            const homeFlag = getFlag(match.homeTeam);
            const awayFlag = getFlag(match.awayTeam);
            
            // Determine match stage based on Game Week or other info
            let matchStage = 'Qualification Stage';
            if (match.gameWeek && match.gameWeek !== 'N/A') {
                if (match.gameWeek === '1' || match.gameWeek === '2' || match.gameWeek === '3') {
                    matchStage = `Group Stage - Matchday ${match.gameWeek}`;
                } else {
                    matchStage = 'Knockout Stage';
                }
            }
            
            matchHtml += `
                <div class="match-card-new">
                    <div class="match-teams">
                        <div class="match-team home">
                            <span class="team-name">${match.homeTeam}</span>
                            ${homeFlag ? `<img class="team-flag" src="${homeFlag}" alt="${match.homeTeam}">` : ''}
                        </div>
                        <div class="match-score">
                            <span class="score">${match.homeScore}</span>
                            <span class="ft-label">FT</span>
                            <span class="score">${match.awayScore}</span>
                        </div>
                        <div class="match-team away">
                            ${awayFlag ? `<img class="team-flag" src="${awayFlag}" alt="${match.awayTeam}">` : ''}
                            <span class="team-name">${match.awayTeam}</span>
                        </div>
                    </div>
                    <div class="match-info">
                        ${matchStage} · Play-off${match.venue ? ' · ' + match.venue : ''}
                    </div>
                </div>
            `;
        });
    });

    matchesContainer.innerHTML = matchHtml || "<p>No matches available.</p>";
}

// Fetch and display players of each team (all are Arab Cup teams from CSV)
async function displayPlayers(countryFilter = '') {
    const playersContainer = document.getElementById("playersList");
    
    try {
        const response = await fetch(`${apiUrl}/api/players/`);
        const players = await response.json();
        
        // Cache all players with normalized data for lineup view
        playersCache = players.map(p => ({
            ...p,
            _country: p["Current Club"] || p.nationality || "",
            _name: getPlayerName(p),
            full_name: p["Full Name"] || p.full_name || getPlayerName(p),
            name: getPlayerName(p),
            position: p.position || "N/A"
        }));
        
        // Filter by country if specified
        let filteredPlayers = playersCache;
        
        if (countryFilter) {
            filteredPlayers = filteredPlayers.filter(p => p._country === countryFilter);
        }
        
        if (filteredPlayers.length === 0) {
            playersContainer.innerHTML = `<p class='placeholder'>${countryFilter ? `No players found for ${countryFilter}` : 'Select a country to view players'}</p>`;
            return;
        }
        
        // Update lineup team selector to current country if a country is selected
        if (countryFilter) {
            const teamSelect = document.getElementById('lineupTeam');
            if (teamSelect) {
                teamSelect.value = countryFilter;
            }
        }
        
        // Categorize by position
        const positionCategories = {
            "Goalkeeper": [],
            "Defender": [],
            "Midfielder": [],
            "Forward": []
        };
        
        filteredPlayers.forEach(player => {
            const pos = (player.position || "").toUpperCase();
            if (pos.includes("GK") || pos.includes("GOALKEEPER")) {
                positionCategories["Goalkeeper"].push(player);
            } else if (pos.includes("DEF") || pos.includes("BACK")) {
                positionCategories["Defender"].push(player);
            } else if (pos.includes("MID")) {
                positionCategories["Midfielder"].push(player);
            } else if (pos.includes("FW") || pos.includes("FORWARD") || pos.includes("STRIKER") || pos.includes("ATTACK")) {
                positionCategories["Forward"].push(player);
            } else {
                positionCategories["Midfielder"].push(player);
            }
        });
        
        const country = countryFilter || "All Teams";
        const flagUrl = countryFilter ? getFlag(countryFilter) : "";
        
        let playerHtml = `
            <div class="squad-header">
                ${flagUrl ? `<img class="squad-flag" src="${flagUrl}" alt="${country}">` : ''}
                <h2>${country} Squad</h2>
            </div>
        `;
        
        Object.keys(positionCategories).forEach(position => {
            const posPlayers = positionCategories[position];
            if (posPlayers.length === 0) return;
            
            playerHtml += `
                <div class="position-section">
                    <h3 class="position-title">${position}s (${posPlayers.length})</h3>
                    <div class="players-grid-simple">
            `;
            
            posPlayers.forEach(player => {
                const flagUrl = getFlag(player._country);
                playerHtml += `
                    <div class="player-card-simple">
                        ${flagUrl ? `<img src="${flagUrl}" alt="${player._country}" class="player-flag-small">` : ''}
                        <div class="player-info-simple">
                            <div class="player-name">${player._name}</div>
                            <div class="player-position">${player.position || 'N/A'}</div>
                        </div>
                    </div>
                `;
            });
            
            playerHtml += `
                    </div>
                </div>
            `;
        });
        
        playersContainer.innerHTML = playerHtml;
        
        // Render the lineup after players are displayed
        if (countryFilter) {
            renderCurrentLineup();
        }
        
    } catch (error) {
        console.error('Error loading players:', error);
        playersContainer.innerHTML = "<p class='placeholder'>Error loading players</p>";
    }
}


// Handle login form submission
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch(`${apiUrl}/api/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    if (response.ok) {
        const data = await response.json();
        jwtToken = data.token; // Store the JWT token (session only)
        document.getElementById('login').style.display = 'none';
        document.getElementById('dashboard').style.display = 'block';
        // Auto-load all data
        await loadAllData();
    } else {
        alert("Invalid credentials");
    }
});

// Fetch and display dashboard stats
async function fetchDashboardStats() {
    // Dashboard stats elements don't exist in HTML, so skip this
    console.log('Dashboard loaded');
}

// Filter matches by country
document.getElementById('countryFilter').addEventListener('change', (e) => {
    const selectedCountry = e.target.value;
    displayMatches(selectedCountry);
});

// Filter players by country
const playersCountryFilterEl = document.getElementById('playersCountryFilter');
if (playersCountryFilterEl) {
    playersCountryFilterEl.addEventListener('change', (e) => {
        displayPlayers(e.target.value);
    });
}

// Auto-load all data from CSV-based API
async function loadAllData() {
    console.log('loadAllData called');
    try {
        // Initialize countries and populate dropdowns first
        await initializeCountries();
        await displayTeams();
        await displayMatches();
        await displayPlayers();
        if (window.StatisticsModule) {
            await StatisticsModule.loadLeaderboards();
        }
        initLineupControls();
        renderCurrentLineup();
        console.log('All data loaded successfully');
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

// Country filter will be populated after login when dashboard loads

// Load teams from database on page load
async function initializeCountries() {
    try {
        const response = await fetch(`${apiUrl}/api/teams/`);
        if (response.ok) {
            const teams = await response.json();
            const allowedCountries = new Set(Object.keys(flagMap));
            // Extract unique allowed countries from teams
            arabCupCountries = [...new Set(teams.map(t => t.country).filter(c => allowedCountries.has(c)))].sort();
            // Populate country filter dropdowns
            populateCountryFilter();
        }
    } catch (error) {
        console.error('Error loading countries:', error);
    }
}

// Country filters will be populated after login when dashboard loads

// Always show login page on page load (JWT is session-only)
window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('login').style.display = 'block';
    document.getElementById('dashboard').style.display = 'none';
});

// ---------------------
// Lineup / Cartography
// ---------------------

// Supported formations with ordered slots
const formations = {
    "4-3-3": ["GK", "LB", "LCB", "RCB", "RB", "LCM", "CM", "RCM", "LW", "ST", "RW"],
    "4-2-3-1": ["GK", "LB", "LCB", "RCB", "RB", "LDM", "RDM", "LAM", "CAM", "RAM", "ST"],
    "3-5-2": ["GK", "LCB", "CB", "RCB", "LWB", "RWB", "LCM", "RCM", "CAM", "ST", "ST2"],
};

// Slot coordinates (percent of pitch width/height)
const slotCoords = {
    "4-3-3": {
        GK: { x: 50, y: 92 },
        LB: { x: 20, y: 75 }, LCB: { x: 40, y: 78 }, RCB: { x: 60, y: 78 }, RB: { x: 80, y: 75 },
        LCM: { x: 35, y: 55 }, CM: { x: 50, y: 50 }, RCM: { x: 65, y: 55 },
        LW: { x: 22, y: 30 }, ST: { x: 50, y: 22 }, RW: { x: 78, y: 30 }
    },
    "4-2-3-1": {
        GK: { x: 50, y: 92 },
        LB: { x: 20, y: 75 }, LCB: { x: 40, y: 78 }, RCB: { x: 60, y: 78 }, RB: { x: 80, y: 75 },
        LDM: { x: 38, y: 60 }, RDM: { x: 62, y: 60 },
        LAM: { x: 32, y: 40 }, CAM: { x: 50, y: 34 }, RAM: { x: 68, y: 40 },
        ST: { x: 50, y: 20 }
    },
    "3-5-2": {
        GK: { x: 50, y: 92 },
        LCB: { x: 35, y: 80 }, CB: { x: 50, y: 78 }, RCB: { x: 65, y: 80 },
        LWB: { x: 20, y: 62 }, RWB: { x: 80, y: 62 },
        LCM: { x: 35, y: 45 }, RCM: { x: 65, y: 45 }, CAM: { x: 50, y: 35 },
        ST: { x: 42, y: 22 }, ST2: { x: 58, y: 22 }
    }
};

function initLineupControls() {
    // Initialize lineup controls on the main page
    const formationSelect = document.getElementById("lineupFormation");
    const teamSelect = document.getElementById("lineupTeam");
    const lineupStatus = document.getElementById("lineupStatus");
    
    if (!formationSelect || !teamSelect || !lineupStatus) {
        console.log('Lineup controls not found in HTML');
        return; // Lineup controls not available
    }
    
    // Populate formation options
    formationSelect.innerHTML = "";
    Object.keys(formations).forEach((f) => {
        const opt = document.createElement("option");
        opt.value = f;
        opt.textContent = f;
        formationSelect.appendChild(opt);
    });
    formationSelect.value = "4-3-3";

    // Populate team options (Arab Cup list ensures display order)
    teamSelect.innerHTML = "";
    arabCupCountries.forEach((country) => {
        const opt = document.createElement("option");
        opt.value = country;
        opt.textContent = country;
        teamSelect.appendChild(opt);
    });

    teamSelect.addEventListener("change", renderCurrentLineup);
    formationSelect.addEventListener("change", renderCurrentLineup);

    // Initial placeholder
    lineupStatus.textContent = "Load players to view the lineup.";
}

function normalizePosition(raw) {
    if (!raw) return "UNK";
    const p = raw.toLowerCase();
    if (p.includes("keeper") || p === "gk") return "GK";
    if (p.includes("back") || p.includes("def")) return "DEF";
    if (p.includes("mid")) return "MID";
    if (p.includes("wing")) return "FWD";
    if (p.includes("striker") || p.includes("forward") || p === "st") return "FWD";
    return "UNK";
}

function slotRole(slotName) {
    if (slotName.startsWith("GK")) return "GK";
    if (slotName.includes("CB") || slotName.includes("B")) return "DEF";
    if (slotName.includes("DM") || slotName.includes("CM") || slotName.includes("AM")) return "MID";
    if (slotName.includes("W") || slotName.includes("ST")) return "FWD";
    return "UNK";
}

function renderCurrentLineup() {
    // Get element references
    const formationSelect = document.getElementById("lineupFormation");
    const teamSelect = document.getElementById("lineupTeam");
    const lineupStatus = document.getElementById("lineupStatus");
    const pitchEl = document.getElementById("pitch");
    const benchEl = document.getElementById("bench");
    
    // Skip if lineup controls don't exist on this page
    if (!teamSelect || !formationSelect || !pitchEl || !benchEl || !lineupStatus) return;
    
    const team = teamSelect.value;
    const formation = formationSelect.value;
    if (!team || !formation) return;

    const slots = formations[formation];
    const coords = slotCoords[formation];
    const teamPlayers = playersCache.filter(p => (p._country || getPlayerCountry(p)) === team);

    // Buckets
    const buckets = { GK: [], DEF: [], MID: [], FWD: [], UNK: [] };
    teamPlayers.forEach(p => {
        const role = normalizePosition(p.position);
        (buckets[role] || buckets.UNK).push(p);
    });

    // Deterministic order
    Object.keys(buckets).forEach(key => buckets[key].sort((a, b) => {
        const nameA = a._name || getPlayerName(a);
        const nameB = b._name || getPlayerName(b);
        return nameA.localeCompare(nameB);
    }));

    const slotAssignments = {};
    const usedIds = new Set();

    slots.forEach(slot => {
        const role = slotRole(slot);
        const primary = buckets[role] || [];
        const fallback = role === "GK" ? [] : buckets.MID; // keep GK strict
        const pickFrom = primary.length ? primary : fallback.length ? fallback : buckets.UNK;
        const player = pickFrom.shift();
        if (player) {
            const normalizedName = player._name || getPlayerName(player);
            slotAssignments[slot] = player;
            usedIds.add(normalizedName);
        }
    });

    const bench = teamPlayers
        .filter(p => !usedIds.has(p._name || getPlayerName(p)))
        .sort((a, b) => (a._name || getPlayerName(a)).localeCompare(b._name || getPlayerName(b)));

    // Render pitch
    pitchEl.innerHTML = "";
    slots.forEach(slot => {
        const coord = coords[slot];
        if (!coord) return;
        const player = slotAssignments[slot];
        const role = slotRole(slot);
        const slotDiv = document.createElement("div");
        slotDiv.className = `slot ${player ? "" : "slot-empty"} role-${role.toLowerCase()}`;
        slotDiv.style.left = coord.x + "%";
        slotDiv.style.top = coord.y + "%";
        slotDiv.title = player ? `${player.full_name || player.name} (${player.position || role})` : `${slot} (empty)`;
        slotDiv.textContent = player ? (player.full_name || player.name).split(" ").slice(0, 2).join(" ") : slot;
        pitchEl.appendChild(slotDiv);
    });

    // Render bench
    benchEl.innerHTML = bench.length ? "" : "<span class='placeholder'>No bench players</span>";
    bench.forEach(p => {
        const chip = document.createElement("div");
        chip.className = "bench-chip";
        chip.textContent = `${p.full_name || p.name} (${p.position || "UNK"})`;
        benchEl.appendChild(chip);
    });

    lineupStatus.textContent = `Showing ${formation} for ${team}`;
}
