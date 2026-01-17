/**
 * Statistics Module - Handles player and team statistics display
 */

const StatisticsModule = {
    gauge(label, value, maxValue) {
        const v = Number(value ?? 0);
        const max = Number(maxValue ?? 0) || 1;
        const pct = Math.max(0, Math.min(100, Math.round((v / max) * 100)));
        return `
            <div class="gauge" style="--fill:${pct}%;">
                <div class="gauge-inner"></div>
                <span class="gauge-value">${Number.isFinite(v) ? v : '-'}</span>
                <small class="gauge-label">${label}</small>
            </div>
        `;
    },

    formatNumber(value, digits = 2) {
        const num = Number(value);
        if (!Number.isFinite(num)) return '-';
        return Math.abs(num % 1) < 1e-9 ? num : num.toFixed(digits);
    },

    flag(country) {
        const map = window.flagMap || {
            "Qatar": "https://flagcdn.com/w40/qa.png",
            "Tunisia": "https://flagcdn.com/w40/tn.png",
            "Syria": "https://flagcdn.com/w40/sy.png",
            "Palestine": "https://flagcdn.com/w40/ps.png",
            "Morocco": "https://flagcdn.com/w40/ma.png",
            "Saudi Arabia": "https://flagcdn.com/w40/sa.png",
            "Oman": "https://flagcdn.com/w40/om.png",
            "Comoros": "https://flagcdn.com/w40/km.png",
            "Egypt": "https://flagcdn.com/w40/eg.png",
            "Jordan": "https://flagcdn.com/w40/jo.png",
            "United Arab Emirates": "https://flagcdn.com/w40/ae.png",
            "UAE": "https://flagcdn.com/w40/ae.png",
            "Kuwait": "https://flagcdn.com/w40/kw.png",
            "Algeria": "https://flagcdn.com/w40/dz.png",
            "Iraq": "https://flagcdn.com/w40/iq.png",
            "Bahrain": "https://flagcdn.com/w40/bh.png",
            "Sudan": "https://flagcdn.com/w40/sd.png",
            "Djibouti": "https://flagcdn.com/w40/dj.png",
            "South Sudan": "https://flagcdn.com/w40/ss.png",
            "Somalia": "https://flagcdn.com/w40/so.png",
            "Yemen": "https://flagcdn.com/w40/ye.png",
            "Libya": "https://flagcdn.com/w40/ly.png",
            "Mauritania": "https://flagcdn.com/w40/mr.png"
        };
        const url = map[country];
        return url ? `<img src="${url}" alt="${country} flag" class="mini-flag" loading="lazy">` : '';
    },

    barRow(label, value, maxValue = 10, suffix = '') {
        const num = Number(value ?? 0);
        const max = Number(maxValue ?? 1) || 1;
        const pct = Math.max(0, Math.min(100, Math.round((num / max) * 100)));
        return `
            <div class="attr-row">
                <span class="attr-label">${label}</span>
                <div class="attr-bar"><span class="attr-fill" style="width:${pct}%"></span></div>
                <span class="attr-value">${Number.isFinite(num) ? this.formatNumber(num) + suffix : '-'}</span>
            </div>
        `;
    },

    attrSection(title, metrics) {
        const visible = metrics.filter(m => Number.isFinite(Number(m.value)) && Number(m.value) !== 0);
        if (!visible.length) return '';
        return `
            <div class="attr-section">
                <div class="attr-title">${title}</div>
                ${visible.map(m => this.barRow(m.label, m.value, m.max, m.suffix)).join('')}
            </div>
        `;
    },

    buildPlayerAttributes(player) {
        const goals = Number(player.goals_overall || 0);
        const assists = Number(player.assists_overall || 0);
        const g90 = Number(player.goals_per_90_overall || 0);
        const xg = Number(player.xg_per_game_overall || 0);
        const shotsOT = Number(player.shots_on_target_per_game_overall || 0);
        const dribbles = Number(player.dribbles_per_game_overall || player.dribbles_successful_per_game_overall || 0);
        const passes = Number(player.passes_per_90_overall || 0);
        const passCmp = Number(player.pass_completion_rate_overall || 0);
        const keyPasses = Number(player.key_passes_per_game_overall || 0);
        const tackles = Number(player.tackles_per_90_overall || 0);
        const inter = Number(player.interceptions_per_game_overall || player.interceptions_per_90_overall || 0);
        const clearances = Number(player.clearances_per_game_overall || 0);
        const blocks = Number(player.blocks_per_game_overall || 0);
        const saves = Number(player.saves_per_game_overall || 0);
        const savePct = Number(player.save_percentage_overall || 0);
        const conceded = Number(player.conceded_per_90_overall || 0);
        const cleanSheets = Number(player.clean_sheets_overall || 0);

        const sections = [];

        sections.push(this.attrSection('Attacking', [
            { label: 'Goals', value: goals, max: Math.max(10, goals) },
            { label: 'G/90', value: g90, max: 1.2 },
            { label: 'Shots OT/90', value: shotsOT, max: 5 },
            { label: 'xG/90', value: xg, max: 1.2 },
            { label: 'Dribbles/90', value: dribbles, max: 7 }
        ]));

        sections.push(this.attrSection('Playmaking', [
            { label: 'Assists', value: assists, max: Math.max(10, assists) },
            { label: 'A/90', value: Number(player.assists_per_90_overall || 0), max: 1.0 },
            { label: 'Key Passes/90', value: keyPasses, max: 5 },
            { label: 'Passes/90', value: passes, max: 100 },
            { label: 'Pass %', value: passCmp, max: 100, suffix: '%' }
        ]));

        sections.push(this.attrSection('Defending', [
            { label: 'Tackles/90', value: tackles, max: 5 },
            { label: 'Inter/90', value: inter, max: 5 },
            { label: 'Clearances', value: clearances, max: 8 },
            { label: 'Blocks', value: blocks, max: 5 }
        ]));

        sections.push(this.attrSection('Goalkeeping', [
            { label: 'Saves/90', value: saves, max: 7 },
            { label: 'Save %', value: savePct, max: 100, suffix: '%' },
            { label: 'Conceded/90', value: conceded, max: 3 },
            { label: 'Clean Sheets', value: cleanSheets, max: Math.max(cleanSheets, 10) }
        ]));

        const combined = sections.filter(Boolean).join('');
        return combined || '<p class="attr-empty">No detailed stats available.</p>';
    },

    /**
     * Load and display leaderboards
     */
    async loadLeaderboards() {
        try {
            const [scorers, assists, defenders, standings] = await Promise.all([
                fetch(`${window.apiUrl || 'http://localhost:5000'}/api/leaderboards/top-scorers`).then(r => r.json()),
                fetch(`${window.apiUrl || 'http://localhost:5000'}/api/leaderboards/top-assists`).then(r => r.json()),
                fetch(`${window.apiUrl || 'http://localhost:5000'}/api/leaderboards/top-defenders`).then(r => r.json()),
                fetch(`${window.apiUrl || 'http://localhost:5000'}/api/leaderboards/standings`).then(r => r.json())
            ]);

            this.displayScorers(scorers.leaderboard);
            this.displayAssists(assists.leaderboard);
            this.displayDefenders(defenders.leaderboard);
            this.displayStandings(standings.standings);
        } catch (error) {
            console.error('Error loading leaderboards:', error);
        }
    },

    displayScorers(scorers) {
        if (!Array.isArray(scorers)) return;
        const container = document.getElementById('scorersBody');
        if (!container) {
            console.warn('scorersBody element not found');
            return;
        }
        // Filter out invalid entries (name is "None" or empty, or aggregate totals with unrealistic goal counts)
        const validScorers = scorers.filter(p => {
            const playerName = (p.full_name || p.name || '').trim().toLowerCase();
            const goals = Number(p.goals_overall || 0);
            return playerName !== 'none' && playerName !== '' && goals <= 20;
        });
        container.innerHTML = validScorers.map((player, idx) => {
            return `
                <tr>
                    <td>${idx + 1}</td>
                    <td>${player.full_name || 'Unknown'}</td>
                    <td>${player['Current Club'] || player.nationality || '-'}</td>
                    <td>${player.position || '-'}</td>
                    <td>${this.formatNumber(player.goals_overall)}</td>
                    <td>${this.formatNumber(player.assists_overall)}</td>
                    <td>${this.formatNumber(player.goals_per_90_overall)}</td>
                </tr>
            `;
        }).join('');
    },

    displayAssists(assists) {
        if (!Array.isArray(assists)) return;
        const container = document.getElementById('assistsBody');
        if (!container) {
            console.warn('assistsBody element not found');
            return;
        }
        // Filter out invalid entries (name is "None" or empty)
        const validAssists = assists.filter(p => {
            const playerName = (p.full_name || p.name || '').trim().toLowerCase();
            return playerName !== 'none' && playerName !== '';
        });
        container.innerHTML = validAssists.map((player, idx) => {
            return `
                <tr>
                    <td>${idx + 1}</td>
                    <td>${player.full_name || 'Unknown'}</td>
                    <td>${player['Current Club'] || player.nationality || '-'}</td>
                    <td>${player.position || '-'}</td>
                    <td>${this.formatNumber(player.assists_overall)}</td>
                    <td>${this.formatNumber(player.goals_overall)}</td>
                    <td>${this.formatNumber(player.assists_per_90_overall)}</td>
                </tr>
            `;
        }).join('');
    },

    displayDefenders(defenders) {
        if (!Array.isArray(defenders)) return;
        const container = document.getElementById('defendersBody');
        if (!container) {
            console.warn('defendersBody element not found');
            return;
        }
        // Filter out invalid entries (name is "None" or empty)
        const validDefenders = defenders.filter(p => {
            const playerName = (p.full_name || p.name || '').trim().toLowerCase();
            return playerName !== 'none' && playerName !== '';
        });
        container.innerHTML = validDefenders.map((player, idx) => {
            const tackles = Number(player.tackles_per_90_overall ?? player.tackles_total_overall ?? 0);
            const inter = Number(player.interceptions_per_90_overall ?? player.interceptions_total_overall ?? player.interceptions_per_game_overall ?? 0);
            const defActions = tackles + inter;
            return `
                <tr>
                    <td>${idx + 1}</td>
                    <td>${player.full_name || 'Unknown'}</td>
                    <td>${player['Current Club'] || player.nationality || '-'}</td>
                    <td>${player.position || '-'}</td>
                    <td>${this.formatNumber(tackles)}</td>
                    <td>${this.formatNumber(inter)}</td>
                    <td>${this.formatNumber(defActions)}</td>
                </tr>
            `;
        }).join('');
    },

    displayStandings(standings) {
        if (!Array.isArray(standings)) return;
        const container = document.getElementById('standingsBody');
        if (!container) {
            console.warn('standingsBody element not found');
            return;
        }
        
        // Filter out invalid/empty entries
        const validStandings = standings.filter(team => {
            const teamName = (team.name || team.country || '').trim().toLowerCase();
            const matchesPlayed = team.matches_played || (team.wins || 0) + (team.draws || 0) + (team.losses || 0);
            
            // Skip if name is "none", empty, or has no matches played
            return teamName !== 'none' && 
                   teamName !== '' && 
                   matchesPlayed > 0;
        });
        
        // Sort standings by points (descending), then by goal difference
        const sortedStandings = [...validStandings].sort((a, b) => {
            const ptsA = a.points || ((a.wins || 0) * 3 + (a.draws || 0));
            const ptsB = b.points || ((b.wins || 0) * 3 + (b.draws || 0));
            if (ptsB !== ptsA) return ptsB - ptsA;
            const gdA = (a.goals_scored || 0) - (a.goals_conceded || 0);
            const gdB = (b.goals_scored || 0) - (b.goals_conceded || 0);
            return gdB - gdA;
        });
        
        container.innerHTML = sortedStandings.map((team, idx) => {
            const gd = (team.goals_scored || 0) - (team.goals_conceded || 0);
            const pts = team.points || ((team.wins || 0) * 3 + (team.draws || 0));
            return `
                <tr>
                    <td>${idx + 1}</td>
                    <td>${team.name || team.country}</td>
                    <td>${team.matches_played || 0}</td>
                    <td>${team.wins || 0}</td>
                    <td>${team.draws || 0}</td>
                    <td>${team.losses || 0}</td>
                    <td>${team.goals_scored || 0}</td>
                    <td>${team.goals_conceded || 0}</td>
                    <td>${gd}</td>
                    <td>${pts}</td>
                </tr>
            `;
        }).join('');
    },

    /**
     * Setup leaderboard tab switching
     */
    setupLeaderboardTabs() {
        document.querySelectorAll('.leaderboard-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                document.querySelectorAll('.leaderboard-content').forEach(content => {
                    content.style.display = 'none';
                });
                document.querySelectorAll('.leaderboard-tab').forEach(t => t.classList.remove('active'));
                const tabName = e.target.dataset.tab;
                document.getElementById(`${tabName}Leaderboard`).style.display = 'block';
                e.target.classList.add('active');
            });
        });
    },

    /**
     * Setup player search
     */
    setupPlayerSearch() {
        const searchInput = document.getElementById('playerSearchInput');
        if (!searchInput) return;
        
        // Add clear button functionality
        let clearBtn = document.getElementById('playerSearchClear');
        if (!clearBtn) {
            clearBtn = document.createElement('button');
            clearBtn.id = 'playerSearchClear';
            clearBtn.className = 'search-clear-btn';
            clearBtn.textContent = '✕';
            clearBtn.style.display = 'none';
            searchInput.parentNode.insertBefore(clearBtn, searchInput.nextSibling);
        }
        
        clearBtn.addEventListener('click', () => {
            searchInput.value = '';
            clearBtn.style.display = 'none';
            this.hidePlayerSearchResults();
            const card = document.getElementById('playerStatsCard');
            if (card) card.style.display = 'none';
        });
        
        // Debounce search
        let debounceTimer;
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            
            // Show/hide clear button
            document.getElementById('playerSearchClear').style.display = query ? 'block' : 'none';
            
            clearTimeout(debounceTimer);
            
            if (query.length >= 2) {
                debounceTimer = setTimeout(() => {
                    this.searchPlayerStats(query);
                }, 200);
            } else {
                this.hidePlayerSearchResults();
            }
        });
        
        // Keyboard navigation
        searchInput.addEventListener('keydown', (e) => {
            const dropdown = document.getElementById('playerSearchResults');
            if (!dropdown || dropdown.style.display === 'none') return;
            
            const items = dropdown.querySelectorAll('.search-result-item');
            let currentIndex = -1;
            
            const selected = dropdown.querySelector('.search-result-item.selected');
            if (selected) {
                currentIndex = Array.from(items).indexOf(selected);
            }
            
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                currentIndex = (currentIndex + 1) % items.length;
                this.selectSearchItemByIndex(items, currentIndex);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                currentIndex = currentIndex <= 0 ? items.length - 1 : currentIndex - 1;
                this.selectSearchItemByIndex(items, currentIndex);
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (selected) {
                    selected.click();
                }
            } else if (e.key === 'Escape') {
                this.hidePlayerSearchResults();
            }
        });
        
        // Close search results when clicking outside
        document.addEventListener('click', (e) => {
            if (e.target !== searchInput && !e.target.closest('.player-search-results') && !e.target.closest('.search-clear-btn')) {
                this.hidePlayerSearchResults();
            }
        });
    },
    
    selectSearchItemByIndex(items, index) {
        items.forEach(item => item.classList.remove('selected'));
        if (items[index]) {
            items[index].classList.add('selected');
            items[index].scrollIntoView({ block: 'nearest' });
        }
    },

    /**
     * Search and display player statistics
     */
    async searchPlayerStats(playerName) {
        try {
            const response = await fetch(`${window.apiUrl || 'http://localhost:5000'}/api/players/`);
            const players = await response.json();

            const allowed = new Set((window.allowedTeamNames || []).map(n => n.replace(' National Team','').trim()));
            const inScope = players.filter(p => !allowed.size || allowed.has((p.nationality || p['Current Club'] || '').trim()));
            
            // Search query - convert to lowercase for case-insensitive matching
            const query = playerName.toLowerCase().trim();
            
            if (query.length === 0) {
                this.hidePlayerSearchResults();
                return;
            }
            
            // Filter players by matching first name, last name, or full name
            const matchingPlayers = inScope.filter(p => {
                const fullName = (p.full_name || p.name || '').toLowerCase();
                const nameParts = fullName.split(' ');
                
                // Match if query appears in full name, first name, or last name
                return fullName.includes(query) || 
                       nameParts.some(part => part.startsWith(query));
            });
            
            if (matchingPlayers.length > 0) {
                this.displayPlayerSearchResults(matchingPlayers, playerName);
            } else {
                this.displayPlayerSearchResults([], playerName);
            }
        } catch (error) {
            console.error('Error searching player:', error);
        }
    },
    
    displayPlayerSearchResults(players, query) {
        let resultsContainer = document.getElementById('playerSearchResults');
        
        if (!resultsContainer) {
            resultsContainer = document.createElement('div');
            resultsContainer.id = 'playerSearchResults';
            resultsContainer.className = 'player-search-results';
            const searchInput = document.getElementById('playerSearchInput');
            if (searchInput) {
                searchInput.parentNode.insertBefore(resultsContainer, searchInput.nextSibling);
            }
        }
        
        if (players.length === 0) {
            resultsContainer.innerHTML = '<div class="search-no-results">No players found</div>';
            resultsContainer.style.display = 'block';
            return;
        }
        
        // Highlight matching text in player names
        const highlightMatch = (text, query) => {
            const regex = new RegExp(`(${query})`, 'gi');
            return text.replace(regex, '<strong>$1</strong>');
        };
        
        resultsContainer.innerHTML = players.slice(0, 10).map(player => {
            const playerJson = JSON.stringify(player).replace(/"/g, '&quot;');
            const fullName = player.full_name || player.name;
            const highlightedName = highlightMatch(fullName, query);
            return `
                <div class="search-result-item" onclick="StatisticsModule.selectPlayerFromSearch('${playerJson}')">
                    <div class="result-name">${highlightedName}</div>
                    <div class="result-meta">${player.position || '-'} • ${player.nationality || '-'}</div>
                </div>
            `;
        }).join('');
        
        resultsContainer.style.display = 'block';
    },
    
    hidePlayerSearchResults() {
        const resultsContainer = document.getElementById('playerSearchResults');
        if (resultsContainer) {
            resultsContainer.style.display = 'none';
        }
    },
    
    selectPlayerFromSearch(playerJson) {
        try {
            const player = JSON.parse(playerJson.replace(/&quot;/g, '"'));
            this.renderPlayerCard(player);
            const searchInput = document.getElementById('playerSearchInput');
            if (searchInput) {
                searchInput.value = player.full_name || player.name;
            }
            this.hidePlayerSearchResults();
        } catch (error) {
            console.error('Error parsing player:', error);
        }
    },

    renderPlayerCard(player) {
        const card = document.getElementById('playerStatsCard');
        if (!card) return;

        const name = player.full_name || player.name || 'Unknown';
        const position = player.position || player.player_type || '-';
        const country = player.nationality || player['Current Club'] || '-';
        const club = player['Current Club'] || country;
        const goals = Number(player.goals_overall || 0);
        const assists = Number(player.assists_overall || 0);
        const rating = Number(player.average_rating_overall || 0);

        const flagHtml = this.flag(country);
        const playerFlagEl = document.getElementById('playerFlag');
        if (playerFlagEl) playerFlagEl.innerHTML = flagHtml;
        
        const playerNameEl = document.getElementById('playerName');
        if (playerNameEl) playerNameEl.textContent = name;
        
        const playerPositionEl = document.getElementById('playerPosition');
        if (playerPositionEl) playerPositionEl.textContent = position;
        
        const playerMetaEl = document.getElementById('playerMeta');
        if (playerMetaEl) playerMetaEl.textContent = `${country} • ${club}`;
        
        const playerGoalsCoreEl = document.getElementById('playerGoalsCore');
        if (playerGoalsCoreEl) playerGoalsCoreEl.textContent = this.formatNumber(goals, 0);
        
        const playerAssistsCoreEl = document.getElementById('playerAssistsCore');
        if (playerAssistsCoreEl) playerAssistsCoreEl.textContent = this.formatNumber(assists, 0);
        
        const playerRatingCoreEl = document.getElementById('playerRatingCore');
        if (playerRatingCoreEl) playerRatingCoreEl.textContent = this.formatNumber(rating, 2);

        const attrs = this.buildPlayerAttributes(player);
        const playerAttributesEl = document.getElementById('playerAttributes');
        if (playerAttributesEl) playerAttributesEl.innerHTML = attrs;

        card.style.display = 'grid';
    },

    /**
     * Load team list for selector
     */
    async loadTeamSelector() {
        try {
            const response = await fetch(`${window.apiUrl || 'http://localhost:5000'}/api/teams/`);
            const teams = await response.json();
            const allowedCountries = new Set(window.allowedTeamNames ? window.allowedTeamNames.map(n => n.replace(' National Team','').trim()) : []);
            const selector = document.getElementById('teamSelect');
            
            if (!selector) {
                console.warn('teamSelect element not found');
                return;
            }
            
            teams
                .filter(team => !allowedCountries.size || allowedCountries.has(team.country))
                .forEach(team => {
                    const option = document.createElement('option');
                    option.value = team.country;
                    option.textContent = team.team_name || `${team.country} National Team`;
                    selector.appendChild(option);
                });

            selector.addEventListener('change', (e) => {
                if (e.target.value) {
                    this.loadTeamStats(e.target.value);
                }
            });
        } catch (error) {
            console.error('Error loading teams:', error);
        }
    },

    /**
     * Load and display team statistics in modern card layout
     */
    async loadTeamStats(teamName) {
        try {
            console.log('Loading stats for team:', teamName);
            const response = await fetch(`${window.apiUrl || 'http://localhost:5000'}/api/teams/`);
            const teams = await response.json();
            const team = teams.find(t => t.country.toLowerCase() === teamName.toLowerCase());
            
            console.log('Found team:', team);
            
            if (team) {
                const statsResponse = await fetch(`${window.apiUrl || 'http://localhost:5000'}/api/statistics/teams/${encodeURIComponent(teamName)}`);
                console.log('Stats response status:', statsResponse.status);
                
                if (!statsResponse.ok) {
                    console.error('Team stats not found, status:', statsResponse.status);
                    return;
                }
                const stats = await statsResponse.json();
                console.log('Stats data:', stats);

                // Extract and normalize stats
                const wins = Number(stats.wins || 0);
                const draws = Number(stats.draws || 0);
                const losses = Number(stats.losses || 0);
                const matchesPlayed = Number(stats.matches_played || (wins + draws + losses));
                const goalsFor = Number(stats.goals_scored || 0);
                const goalsAgainst = Number(stats.goals_conceded || 0);
                const goalDiff = goalsFor - goalsAgainst;
                const points = Number(stats.points || (wins * 3 + draws));
                const cleanSheetsPct = Number(stats.clean_sheets_percentage || stats.clean_sheet_percentage || 0);
                const winPct = matchesPlayed > 0 ? Math.round((wins / matchesPlayed) * 100) : 0;
                
                // Calculate ratings (0-10 scale)
                const attackRating = matchesPlayed > 0 ? Math.min(10, (goalsFor / matchesPlayed * 2).toFixed(1)) : 0;
                const defRating = matchesPlayed > 0 ? Math.min(10, (cleanSheetsPct / 10).toFixed(1)) : 0;
                
                // Calculate ranking based on all teams' points
                const standingsResponse = await fetch(`${window.apiUrl || 'http://localhost:5000'}/api/leaderboards/standings`);
                const standingsData = await standingsResponse.json();
                let ranking = '-';
                
                if (standingsData && standingsData.standings) {
                    // Filter and sort standings
                    const validStandings = standingsData.standings.filter(t => {
                        const tName = (t.name || t.country || '').trim().toLowerCase();
                        const tMatches = t.matches_played || (t.wins || 0) + (t.draws || 0) + (t.losses || 0);
                        return tName !== 'none' && tName !== '' && tMatches > 0;
                    });
                    
                    const sortedForRanking = validStandings.sort((a, b) => {
                        const ptsA = a.points || ((a.wins || 0) * 3 + (a.draws || 0));
                        const ptsB = b.points || ((b.wins || 0) * 3 + (b.draws || 0));
                        if (ptsB !== ptsA) return ptsB - ptsA;
                        const gdA = (a.goals_scored || 0) - (a.goals_conceded || 0);
                        const gdB = (b.goals_scored || 0) - (b.goals_conceded || 0);
                        return gdB - gdA;
                    });
                    
                    const rankIndex = sortedForRanking.findIndex(t => (t.country || t.name).toLowerCase() === teamName.toLowerCase());
                    if (rankIndex >= 0) {
                        ranking = rankIndex + 1;
                    }
                }

                const card = document.getElementById('teamStatsCard');
                console.log('Card element:', card);
                
                if (!card) {
                    console.error('teamStatsCard element not found');
                    return;
                }
                
                // Update header - all with null checks
                const teamNameEl = document.getElementById('teamName');
                if (teamNameEl) {
                    teamNameEl.textContent = teamName;
                } else {
                    console.warn('teamName element not found');
                }
                
                // Display ranking
                const rankingEl = document.getElementById('teamRanking');
                if (rankingEl) {
                    rankingEl.textContent = `#${ranking}`;
                }
                
                // Set team badge emoji based on tournament performance
                let badge = '⚪';
                if (teamName === 'Morocco') badge = '🥇';
                else if (teamName === 'Jordan') badge = '🥈';
                else if (teamName === 'Tunisia') badge = '🥉';
                const badgeEl = document.getElementById('teamBadge');
                if (badgeEl) {
                    badgeEl.textContent = badge;
                } else {
                    console.warn('teamBadge element not found');
                }

                // ROW 1: Key Metrics
                // Record: W-D-L format
                const recordEl = document.getElementById('teamRecord');
                if (recordEl) recordEl.textContent = `${wins}-${draws}-${losses}`;
                
                const recordDetailEl = document.getElementById('teamRecordDetail');
                if (recordDetailEl) recordDetailEl.textContent = `${wins}W ${draws}D ${losses}L`;
                
                // Points
                const pointsEl = document.getElementById('teamPointsValue');
                if (pointsEl) pointsEl.textContent = points;
                
                // Goal Difference with color coding
                const gdElement = document.getElementById('teamGD');
                const gdIconElement = document.getElementById('gdIcon');
                const gdStatusElement = document.getElementById('gdStatus');
                
                if (gdElement) {
                    gdElement.textContent = goalDiff >= 0 ? `+${goalDiff}` : `${goalDiff}`;
                }
                
                if (goalDiff > 0) {
                    if (gdElement) gdElement.style.color = '#10b981';
                    if (gdIconElement) gdIconElement.textContent = '↑';
                    if (gdStatusElement) gdStatusElement.textContent = 'Positive';
                } else if (goalDiff < 0) {
                    if (gdElement) gdElement.style.color = '#ef4444';
                    if (gdIconElement) gdIconElement.textContent = '↓';
                    if (gdStatusElement) gdStatusElement.textContent = 'Negative';
                } else {
                    if (gdElement) gdElement.style.color = '#f59e0b';
                    if (gdIconElement) gdIconElement.textContent = '→';
                    if (gdStatusElement) gdStatusElement.textContent = 'Neutral';
                }

                // ROW 2: Goals
                const goalsForEl = document.getElementById('teamGoalsFor');
                if (goalsForEl) goalsForEl.textContent = goalsFor;
                
                const goalsAgainstEl = document.getElementById('teamGoalsAgainst');
                if (goalsAgainstEl) goalsAgainstEl.textContent = goalsAgainst;
                
                const ratioEl = document.getElementById('teamRatio');
                if (ratioEl) ratioEl.textContent = `${goalsFor}:${goalsAgainst}`;

                // ROW 3: Performance (Progress Bars)
                console.log('Updating progress bars...');
                const winPercentageFill = document.getElementById('winPercentageFill');
                if (winPercentageFill) {
                    winPercentageFill.style.width = winPct + '%';
                } else {
                    console.warn('winPercentageFill element not found');
                }
                
                const winPctEl = document.getElementById('teamWinPct');
                if (winPctEl) {
                    winPctEl.textContent = winPct + '%';
                } else {
                    console.warn('teamWinPct element not found');
                }

                const cleanSheetsFill = document.getElementById('cleanSheetsFill');
                if (cleanSheetsFill) {
                    cleanSheetsFill.style.width = cleanSheetsPct + '%';
                } else {
                    console.warn('cleanSheetsFill element not found');
                }
                
                const cleanSheetsEl = document.getElementById('teamCleanSheets');
                if (cleanSheetsEl) {
                    cleanSheetsEl.textContent = this.formatNumber(cleanSheetsPct, 1) + '%';
                } else {
                    console.warn('teamCleanSheets element not found');
                }

                // ROW 4: Ratings
                console.log('Updating ratings...');
                const attackRatingEl = document.getElementById('teamAttackRating');
                if (attackRatingEl) {
                    attackRatingEl.textContent = this.formatNumber(attackRating, 1);
                } else {
                    console.warn('teamAttackRating element not found');
                }
                
                const attackBarMini = document.getElementById('attackBarMini');
                if (attackBarMini) {
                    attackBarMini.style.width = (attackRating / 10 * 100) + '%';
                } else {
                    console.warn('attackBarMini element not found');
                }

                const defRatingEl = document.getElementById('teamDefRating');
                if (defRatingEl) {
                    defRatingEl.textContent = this.formatNumber(defRating, 1);
                } else {
                    console.warn('teamDefRating element not found');
                }
                
                const defenseBarMini = document.getElementById('defenseBarMini');
                if (defenseBarMini) {
                    defenseBarMini.style.width = (defRating / 10 * 100) + '%';
                } else {
                    console.warn('defenseBarMini element not found');
                }

                if (card) {
                    card.style.display = 'block';
                    console.log('Stats card displayed successfully');
                } else {
                    console.error('Cannot display card - element is null');
                }
            } else {
                console.error('Team not found:', teamName);
            }
        } catch (error) {
            console.error('Error loading team stats:', error);
        }
    }
};

/**
 * Initialize statistics module when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('statistics')) {
        StatisticsModule.loadLeaderboards();
        StatisticsModule.setupLeaderboardTabs();
        StatisticsModule.setupPlayerSearch();
        StatisticsModule.loadTeamSelector();
    }
});
