const apiUrl = "http://localhost:5000"; // Backend URL
let jwtToken = ""; // Store the JWT token
let teamsLoaded = false;
let matchesLoaded = false;
let playersLoaded = false;

// Caches to reuse data for lineup view
let teamsCache = [];
let playersCache = [];

// List of Arab Cup countries
const arabCupCountries = [
    "Qatar", "Tunisia", "Syria", "Palestine", "Morocco", "Saudi Arabia", "Oman", "Comoros",
    "Egypt", "Jordan", "United Arab Emirates", "Kuwait", "Algeria", "Iraq", "Bahrain", "Sudan"
];

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
    "Kuwait": "https://flagcdn.com/w80/kw.png",
    "Algeria": "https://flagcdn.com/w80/dz.png",
    "Iraq": "https://flagcdn.com/w80/iq.png",
    "Bahrain": "https://flagcdn.com/w80/bh.png",
    "Sudan": "https://flagcdn.com/w80/sd.png"
};

const flagEmojiFallback = "🏴";

function getFlag(country) {
    return flagMap[country] || "";
}

// Function to display team flags and names
async function displayTeams() {
    const response = await fetch(`${apiUrl}/api/teams/`);
    const teams = await response.json();
    teamsCache = teams; // cache
    const teamsContainer = document.getElementById("teamFlags");

    // Clear previous content
    teamsContainer.innerHTML = "";

    if (!teamsLoaded) {
        teamsContainer.innerHTML = "<p class='placeholder'>Click \"Sync Teams\" to load teams.</p>";
        return;
    }

    // Filter teams to display only Arab Cup teams
    const filteredTeams = teams.filter(team => arabCupCountries.includes(team.country));

    // Generate HTML for teams
    filteredTeams.forEach(team => {
        const teamCard = document.createElement("div");
        teamCard.classList.add("team-card");

        const flagUrl = getFlag(team.country) || team.badge;
        const flagImg = flagUrl ? `<img class="flag-icon" src="${flagUrl}" alt="${team.name} flag" loading="lazy">` : flagEmojiFallback;

        teamCard.innerHTML = `
            ${flagImg}
            <h4>${team.name}</h4>
            <p class="team-country">${team.country}</p>
        `;
        teamsContainer.appendChild(teamCard);
    });
}

// Populate the dropdown filter with countries
function populateCountryFilter() {
    const countryFilter = document.getElementById("countryFilter");
    countryFilter.innerHTML = "<option value=''>Display All</option>"; // Add "Display All"
    arabCupCountries.forEach(country => {
        const option = document.createElement("option");
        option.value = country;
        option.textContent = country;
        countryFilter.appendChild(option);
    });
}

// Display Arab Cup Countries Table with Flags
function displayArabCountries() {
    const countriesTable = document.getElementById("countriesTable").getElementsByTagName('tbody')[0];
    arabCupCountries.forEach(country => {
        const row = countriesTable.insertRow();
        const flagUrl = getFlag(country);
        row.innerHTML = `
            <td>${flagUrl ? `<img class="flag-icon" src="${flagUrl}" alt="${country} flag" loading="lazy">` : flagEmojiFallback}</td>
            <td>${country}</td>
        `;
    });
}

// Fetch and display all matches
async function displayMatches(country = '') {
    const response = await fetch(`${apiUrl}/api/matches/`);
    const matches = await response.json();
    const matchesContainer = document.getElementById("allMatches");

    if (!matchesLoaded) {
        matchesContainer.innerHTML = "<p class='placeholder'>Click \"Sync Matches\" to load matches.</p>";
        return;
    }

    let matchHtml = "";
    matches.forEach(match => {
        if (!country || match.home_team === country || match.away_team === country) {
            matchHtml += `
                <div class="match-card">
                    <h4>${match.home_team} vs ${match.away_team}</h4>
                    <p>${match.date} | Score: ${match.home_score} - ${match.away_score}</p>
                </div>
            `;
        }
    });
    matchesContainer.innerHTML = matchHtml;
}

// Fetch and display players of each team (only Arab Cup teams)
async function displayPlayers() {
    const response = await fetch(`${apiUrl}/api/players/`);
    const players = await response.json();
    playersCache = players; // cache
    const playersContainer = document.getElementById("playersList");

    if (!playersLoaded) {
        playersContainer.innerHTML = "<p class='placeholder'>Click \"Sync Players\" to load players.</p>";
        return;
    }

    // Filter players based on Arab Cup teams
    const filteredPlayers = players.filter(player => player.team && arabCupCountries.includes(player.team));
    
    // Group players by country
    const playersByCountry = {};
    filteredPlayers.forEach(player => {
        if (!playersByCountry[player.team]) {
            playersByCountry[player.team] = [];
        }
        playersByCountry[player.team].push(player);
    });

    // Sort countries alphabetically
    const sortedCountries = Object.keys(playersByCountry).sort();

    let playerHtml = "";
    sortedCountries.forEach(country => {
        const flagUrl = getFlag(country);
        const flag = flagUrl ? `<img class="flag-icon" src="${flagUrl}" alt="${country} flag" loading="lazy">` : flagEmojiFallback;

        playerHtml += `<div class="country-section">
            <h3>${flag} ${country}</h3>
            <div class="players-grid">`;
        
        playersByCountry[country].forEach(player => {
            playerHtml += `
                <div class="player-card">
                    <h4>${player.name}</h4>
                    <p>${player.position || 'N/A'}</p>
                </div>
            `;
        });
        
        playerHtml += `</div></div>`;
    });
    
    playersContainer.innerHTML = playerHtml || "<p>No players data available. Click 'Sync Players' to load data.</p>";

    if (playersLoaded) {
        renderCurrentLineup();
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
        jwtToken = data.token; // Store the JWT token
        document.getElementById('login').style.display = 'none';
        document.getElementById('syncForms').style.display = 'block';
        document.getElementById('dashboard').style.display = 'block';
        displayArabCountries(); // Display Arab Cup countries with flags
        displayTeams(); // Placeholder until sync
        displayMatches(); // Placeholder until sync
        displayPlayers(); // Placeholder until sync
        initLineupControls();
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

// Helper function to show sync status
function showSyncStatus(message, progress = 0) {
    const statusDiv = document.getElementById('syncStatus');
    const statusMsg = document.getElementById('statusMessage');
    const progressFill = document.getElementById('progressFill');
    
    statusDiv.style.display = 'block';
    statusMsg.textContent = message;
    progressFill.style.width = progress + '%';
}

// Helper function to hide sync status
function hideSyncStatus() {
    const statusDiv = document.getElementById('syncStatus');
    statusDiv.style.display = 'none';
}

// Helper function to disable all sync buttons
function disableSyncButtons() {
    document.getElementById('syncTeamsBtn').disabled = true;
    document.getElementById('syncMatchesBtn').disabled = true;
    document.getElementById('syncPlayersBtn').disabled = true;
}

// Helper function to enable all sync buttons
function enableSyncButtons() {
    document.getElementById('syncTeamsBtn').disabled = false;
    document.getElementById('syncMatchesBtn').disabled = false;
    document.getElementById('syncPlayersBtn').disabled = false;
}

// Sync Teams Button
document.getElementById('syncTeamsBtn').addEventListener('click', async () => {
    disableSyncButtons();
    showSyncStatus('Starting teams sync...', 25);
    
    try {
        showSyncStatus('Fetching teams from TheSportsDB...', 50);
        const response = await fetch(`${apiUrl}/api/teams/sync`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${jwtToken}` }
        });
        
        if (response.ok) {
            showSyncStatus('Teams synced successfully! 🎉', 100);
            teamsLoaded = true;
            await displayTeams();
            setTimeout(() => {
                hideSyncStatus();
                alert('Teams synced successfully!');
            }, 1500);
        } else {
            showSyncStatus('Failed to sync teams ❌', 0);
            setTimeout(() => hideSyncStatus(), 2000);
            alert('Failed to sync teams');
        }
    } catch (error) {
        showSyncStatus('Error syncing teams ❌', 0);
        setTimeout(() => hideSyncStatus(), 2000);
        console.error(error);
    }
    enableSyncButtons();
});

// Sync Matches Button
document.getElementById('syncMatchesBtn').addEventListener('click', async () => {
    disableSyncButtons();
    showSyncStatus('Starting matches sync...', 25);
    
    try {
        showSyncStatus('Fetching matches from TheSportsDB...', 50);
        const response = await fetch(`${apiUrl}/api/matches/sync`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${jwtToken}` }
        });
        
        if (response.ok) {
            showSyncStatus('Matches synced successfully! 🎉', 100);
            matchesLoaded = true;
            await displayMatches();
            setTimeout(() => {
                hideSyncStatus();
                alert('Matches synced successfully!');
            }, 1500);
        } else {
            showSyncStatus('Failed to sync matches ❌', 0);
            setTimeout(() => hideSyncStatus(), 2000);
            alert('Failed to sync matches');
        }
    } catch (error) {
        showSyncStatus('Error syncing matches ❌', 0);
        setTimeout(() => hideSyncStatus(), 2000);
        console.error(error);
    }
    enableSyncButtons();
});

// Sync Players Button
document.getElementById('syncPlayersBtn').addEventListener('click', async () => {
    disableSyncButtons();
    showSyncStatus('Starting players sync... This may take a minute ⏳', 10);
    
    try {
        showSyncStatus('Fetching players from all teams... This may take a minute ⏳', 50);
        const response = await fetch(`${apiUrl}/api/players/sync`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${jwtToken}` }
        });
        
        if (response.ok) {
            showSyncStatus('Saving players to database...', 75);
            await new Promise(resolve => setTimeout(resolve, 1000));
            showSyncStatus('Players synced successfully! 🎉', 100);
            playersLoaded = true;
            await displayPlayers();
            setTimeout(() => {
                hideSyncStatus();
                alert('Players synced successfully!');
            }, 1500);
        } else {
            showSyncStatus('Failed to sync players ❌', 0);
            setTimeout(() => hideSyncStatus(), 2000);
            alert('Failed to sync players');
        }
    } catch (error) {
        showSyncStatus('Error syncing players ❌', 0);
        setTimeout(() => hideSyncStatus(), 2000);
        console.error(error);
    }
    enableSyncButtons();
});

populateCountryFilter(); // Populate the country filter dropdown on page load

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

const formationSelect = document.getElementById("lineupFormation");
const teamSelect = document.getElementById("lineupTeam");
const lineupStatus = document.getElementById("lineupStatus");
const pitchEl = document.getElementById("pitch");
const benchEl = document.getElementById("bench");

function initLineupControls() {
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
    if (!playersLoaded) {
        lineupStatus.textContent = "Load players to view the lineup.";
        pitchEl.innerHTML = "";
        benchEl.innerHTML = "";
        return;
    }

    const team = teamSelect.value;
    const formation = formationSelect.value;
    if (!team || !formation) return;

    const slots = formations[formation];
    const coords = slotCoords[formation];
    const teamPlayers = playersCache.filter(p => p.team === team);

    // Buckets
    const buckets = { GK: [], DEF: [], MID: [], FWD: [], UNK: [] };
    teamPlayers.forEach(p => {
        const role = normalizePosition(p.position);
        (buckets[role] || buckets.UNK).push(p);
    });

    // Deterministic order
    Object.keys(buckets).forEach(key => buckets[key].sort((a, b) => a.name.localeCompare(b.name)));

    const slotAssignments = {};
    const usedIds = new Set();

    slots.forEach(slot => {
        const role = slotRole(slot);
        const primary = buckets[role] || [];
        const fallback = role === "GK" ? [] : buckets.MID; // keep GK strict
        const pickFrom = primary.length ? primary : fallback.length ? fallback : buckets.UNK;
        const player = pickFrom.shift();
        if (player) {
            slotAssignments[slot] = player;
            usedIds.add(player.name);
        }
    });

    const bench = teamPlayers.filter(p => !usedIds.has(p.name)).sort((a, b) => a.name.localeCompare(b.name));

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
        slotDiv.title = player ? `${player.name} (${player.position || role})` : `${slot} (empty)`;
        slotDiv.textContent = player ? player.name.split(" ").slice(0, 2).join(" ") : slot;
        pitchEl.appendChild(slotDiv);
    });

    // Render bench
    benchEl.innerHTML = bench.length ? "" : "<span class='placeholder'>No bench players</span>";
    bench.forEach(p => {
        const chip = document.createElement("div");
        chip.className = "bench-chip";
        chip.textContent = `${p.name} (${p.position || "UNK"})`;
        benchEl.appendChild(chip);
    });

    lineupStatus.textContent = `Showing ${formation} for ${team}`;
}
