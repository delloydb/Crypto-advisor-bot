import numpy as np
from datetime import datetime

class SustainabilityScorer:
    def __init__(self):
        # Define sustainability criteria and weights
        self.criteria_weights = {
            'energy_efficiency': 0.40,  # 40% weight
            'governance': 0.30,         # 30% weight
            'innovation': 0.20,         # 20% weight
            'transparency': 0.10        # 10% weight
        }
        
        # Define cryptocurrency sustainability profiles
        self.crypto_profiles = {
            'bitcoin': {
                'consensus': 'proof_of_work',
                'energy_intensity': 'very_high',
                'governance_model': 'decentralized',
                'environmental_initiatives': 'limited',
                'innovation_focus': 'store_of_value',
                'transparency': 'high',
                'carbon_neutral_goal': False,
                'renewable_energy_usage': 'medium'
            },
            'ethereum': {
                'consensus': 'proof_of_stake',
                'energy_intensity': 'low',
                'governance_model': 'developer_led',
                'environmental_initiatives': 'strong',
                'innovation_focus': 'smart_contracts',
                'transparency': 'high',
                'carbon_neutral_goal': True,
                'renewable_energy_usage': 'high'
            },
            'cardano': {
                'consensus': 'proof_of_stake',
                'energy_intensity': 'very_low',
                'governance_model': 'democratic',
                'environmental_initiatives': 'strong',
                'innovation_focus': 'sustainability',
                'transparency': 'very_high',
                'carbon_neutral_goal': True,
                'renewable_energy_usage': 'very_high'
            },
            'polkadot': {
                'consensus': 'nominated_proof_of_stake',
                'energy_intensity': 'very_low',
                'governance_model': 'democratic',
                'environmental_initiatives': 'strong',
                'innovation_focus': 'interoperability',
                'transparency': 'high',
                'carbon_neutral_goal': True,
                'renewable_energy_usage': 'high'
            },
            'solana': {
                'consensus': 'proof_of_history',
                'energy_intensity': 'low',
                'governance_model': 'foundation_led',
                'environmental_initiatives': 'medium',
                'innovation_focus': 'performance',
                'transparency': 'medium',
                'carbon_neutral_goal': True,
                'renewable_energy_usage': 'medium'
            },
            'chainlink': {
                'consensus': 'proof_of_stake',
                'energy_intensity': 'low',
                'governance_model': 'decentralized',
                'environmental_initiatives': 'medium',
                'innovation_focus': 'oracles',
                'transparency': 'medium',
                'carbon_neutral_goal': False,
                'renewable_energy_usage': 'medium'
            },
            'litecoin': {
                'consensus': 'proof_of_work',
                'energy_intensity': 'high',
                'governance_model': 'decentralized',
                'environmental_initiatives': 'limited',
                'innovation_focus': 'payments',
                'transparency': 'medium',
                'carbon_neutral_goal': False,
                'renewable_energy_usage': 'medium'
            },
            'dogecoin': {
                'consensus': 'proof_of_work',
                'energy_intensity': 'high',
                'governance_model': 'community',
                'environmental_initiatives': 'limited',
                'innovation_focus': 'meme',
                'transparency': 'medium',
                'carbon_neutral_goal': False,
                'renewable_energy_usage': 'low'
            },
            'algorand': {
                'consensus': 'pure_proof_of_stake',
                'energy_intensity': 'very_low',
                'governance_model': 'democratic',
                'environmental_initiatives': 'very_strong',
                'innovation_focus': 'sustainability',
                'transparency': 'very_high',
                'carbon_neutral_goal': True,
                'renewable_energy_usage': 'very_high'
            },
            'matic-network': {
                'consensus': 'proof_of_stake',
                'energy_intensity': 'low',
                'governance_model': 'democratic',
                'environmental_initiatives': 'strong',
                'innovation_focus': 'scaling',
                'transparency': 'high',
                'carbon_neutral_goal': True,
                'renewable_energy_usage': 'high'
            }
        }
        
        # Scoring scales
        self.energy_scores = {
            'very_low': 95,
            'low': 80,
            'medium': 60,
            'high': 30,
            'very_high': 10
        }
        
        self.governance_scores = {
            'democratic': 90,
            'decentralized': 80,
            'developer_led': 70,
            'foundation_led': 60,
            'community': 75
        }
        
        self.initiative_scores = {
            'very_strong': 95,
            'strong': 80,
            'medium': 60,
            'limited': 30,
            'none': 10
        }
        
        self.transparency_scores = {
            'very_high': 95,
            'high': 80,
            'medium': 60,
            'low': 30,
            'very_low': 10
        }
        
        self.renewable_energy_scores = {
            'very_high': 95,
            'high': 80,
            'medium': 60,
            'low': 30,
            'very_low': 10
        }
    
    def calculate_sustainability_score(self, crypto_id):
        """Calculate comprehensive sustainability score for a cryptocurrency"""
        # Get crypto profile or use default
        profile = self.crypto_profiles.get(crypto_id.lower(), self._get_default_profile())
        
        # Calculate individual scores
        energy_score = self._calculate_energy_efficiency_score(profile)
        governance_score = self._calculate_governance_score(profile)
        innovation_score = self._calculate_innovation_score(profile)
        transparency_score = self._calculate_transparency_score(profile)
        
        # Calculate weighted total score
        total_score = (
            energy_score * self.criteria_weights['energy_efficiency'] +
            governance_score * self.criteria_weights['governance'] +
            innovation_score * self.criteria_weights['innovation'] +
            transparency_score * self.criteria_weights['transparency']
        )
        
        # Get crypto name for display
        crypto_name = self._get_crypto_display_name(crypto_id)
        
        # Get key sustainability features
        key_features = self._get_key_features(profile)
        
        return {
            'crypto_id': crypto_id,
            'name': crypto_name,
            'total_score': round(total_score, 1),
            'energy_efficiency': round(energy_score, 1),
            'governance': round(governance_score, 1),
            'innovation': round(innovation_score, 1),
            'transparency': round(transparency_score, 1),
            'key_features': key_features,
            'carbon_neutral_goal': profile.get('carbon_neutral_goal', False),
            'consensus_mechanism': profile.get('consensus', 'unknown').replace('_', ' ').title()
        }
    
    def _calculate_energy_efficiency_score(self, profile):
        """Calculate energy efficiency score"""
        base_score = self.energy_scores.get(profile.get('energy_intensity', 'medium'), 60)
        
        # Bonus for renewable energy usage
        renewable_bonus = self.renewable_energy_scores.get(
            profile.get('renewable_energy_usage', 'medium'), 60
        ) * 0.2  # 20% weight for renewable energy
        
        # Bonus for carbon neutral goals
        carbon_bonus = 10 if profile.get('carbon_neutral_goal', False) else 0
        
        # Consensus mechanism adjustment
        consensus = profile.get('consensus', 'unknown')
        if consensus in ['proof_of_stake', 'nominated_proof_of_stake', 'pure_proof_of_stake']:
            consensus_bonus = 15
        elif consensus == 'proof_of_history':
            consensus_bonus = 10
        elif consensus == 'proof_of_work':
            consensus_bonus = -20
        else:
            consensus_bonus = 0
        
        total_score = base_score + renewable_bonus + carbon_bonus + consensus_bonus
        return min(100, max(0, total_score))  # Clamp between 0-100
    
    def _calculate_governance_score(self, profile):
        """Calculate governance score"""
        base_score = self.governance_scores.get(profile.get('governance_model', 'decentralized'), 70)
        
        # Bonus for transparency
        transparency = profile.get('transparency', 'medium')
        transparency_bonus = (self.transparency_scores.get(transparency, 60) - 60) * 0.3
        
        # Bonus for environmental initiatives
        initiatives = profile.get('environmental_initiatives', 'medium')
        initiative_bonus = (self.initiative_scores.get(initiatives, 60) - 60) * 0.2
        
        total_score = base_score + transparency_bonus + initiative_bonus
        return min(100, max(0, total_score))
    
    def _calculate_innovation_score(self, profile):
        """Calculate innovation score"""
        innovation_focus = profile.get('innovation_focus', 'general')
        
        # Base scores for different innovation focuses
        innovation_base_scores = {
            'sustainability': 90,
            'smart_contracts': 85,
            'interoperability': 80,
            'scaling': 80,
            'performance': 75,
            'oracles': 75,
            'store_of_value': 70,
            'payments': 65,
            'privacy': 75,
            'meme': 30,
            'general': 60
        }
        
        base_score = innovation_base_scores.get(innovation_focus, 60)
        
        # Bonus for environmental focus
        if innovation_focus in ['sustainability', 'scaling']:
            environmental_bonus = 10
        else:
            environmental_bonus = 0
        
        # Bonus for carbon neutral goals
        carbon_bonus = 5 if profile.get('carbon_neutral_goal', False) else 0
        
        total_score = base_score + environmental_bonus + carbon_bonus
        return min(100, max(0, total_score))
    
    def _calculate_transparency_score(self, profile):
        """Calculate transparency score"""
        base_score = self.transparency_scores.get(profile.get('transparency', 'medium'), 60)
        
        # Bonus for strong environmental initiatives (shows commitment)
        initiatives = profile.get('environmental_initiatives', 'medium')
        if initiatives in ['strong', 'very_strong']:
            initiative_bonus = 10
        else:
            initiative_bonus = 0
        
        # Bonus for democratic governance (usually more transparent)
        governance = profile.get('governance_model', 'decentralized')
        if governance == 'democratic':
            governance_bonus = 5
        else:
            governance_bonus = 0
        
        total_score = base_score + initiative_bonus + governance_bonus
        return min(100, max(0, total_score))
    
    def _get_default_profile(self):
        """Get default profile for unknown cryptocurrencies"""
        return {
            'consensus': 'unknown',
            'energy_intensity': 'medium',
            'governance_model': 'decentralized',
            'environmental_initiatives': 'limited',
            'innovation_focus': 'general',
            'transparency': 'medium',
            'carbon_neutral_goal': False,
            'renewable_energy_usage': 'medium'
        }
    
    def _get_crypto_display_name(self, crypto_id):
        """Get display name for cryptocurrency"""
        name_mappings = {
            'bitcoin': 'Bitcoin',
            'ethereum': 'Ethereum',
            'cardano': 'Cardano',
            'polkadot': 'Polkadot',
            'solana': 'Solana',
            'chainlink': 'Chainlink',
            'litecoin': 'Litecoin',
            'dogecoin': 'Dogecoin',
            'algorand': 'Algorand',
            'matic-network': 'Polygon'
        }
        
        return name_mappings.get(crypto_id.lower(), crypto_id.title())
    
    def _get_key_features(self, profile):
        """Get key sustainability features for display"""
        features = []
        
        # Consensus mechanism
        consensus = profile.get('consensus', 'unknown')
        if consensus != 'unknown':
            features.append(f"{consensus.replace('_', ' ').title()} consensus")
        
        # Energy efficiency
        energy = profile.get('energy_intensity', 'medium')
        if energy in ['very_low', 'low']:
            features.append("Energy efficient")
        
        # Carbon goals
        if profile.get('carbon_neutral_goal', False):
            features.append("Carbon neutral goal")
        
        # Renewable energy
        renewable = profile.get('renewable_energy_usage', 'medium')
        if renewable in ['high', 'very_high']:
            features.append("High renewable energy usage")
        
        # Environmental initiatives
        initiatives = profile.get('environmental_initiatives', 'medium')
        if initiatives in ['strong', 'very_strong']:
            features.append("Strong environmental initiatives")
        
        # Governance
        governance = profile.get('governance_model', 'decentralized')
        if governance == 'democratic':
            features.append("Democratic governance")
        
        return ', '.join(features) if features else 'Standard cryptocurrency features'
    
    def compare_sustainability_scores(self, crypto_ids):
        """Compare sustainability scores for multiple cryptocurrencies"""
        comparisons = []
        
        for crypto_id in crypto_ids:
            score_data = self.calculate_sustainability_score(crypto_id)
            comparisons.append(score_data)
        
        # Sort by total score (highest first)
        comparisons.sort(key=lambda x: x['total_score'], reverse=True)
        
        return comparisons
    
    def get_sustainability_recommendations(self, risk_tolerance='Moderate'):
        """Get sustainability-focused cryptocurrency recommendations"""
        # Get all available crypto profiles
        all_cryptos = list(self.crypto_profiles.keys())
        
        # Calculate scores for all
        scored_cryptos = []
        for crypto_id in all_cryptos:
            score_data = self.calculate_sustainability_score(crypto_id)
            scored_cryptos.append(score_data)
        
        # Sort by sustainability score
        scored_cryptos.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Filter based on risk tolerance
        recommendations = []
        
        if risk_tolerance == 'Conservative':
            # Focus on top sustainability scores and established cryptos
            for crypto in scored_cryptos:
                if crypto['total_score'] >= 70 and crypto['crypto_id'] in ['bitcoin', 'ethereum', 'cardano']:
                    recommendations.append(crypto)
        
        elif risk_tolerance == 'Moderate':
            # Include more options with good sustainability scores
            for crypto in scored_cryptos:
                if crypto['total_score'] >= 60:
                    recommendations.append(crypto)
        
        else:  # Aggressive
            # Include all options, even experimental sustainable projects
            recommendations = scored_cryptos
        
        return recommendations[:8]  # Return top 8 recommendations
    
    def get_sustainability_report(self):
        """Generate a comprehensive sustainability report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'methodology': {
                'criteria': list(self.criteria_weights.keys()),
                'weights': self.criteria_weights,
                'total_cryptos_analyzed': len(self.crypto_profiles)
            },
            'top_sustainable_cryptos': [],
            'consensus_analysis': {},
            'energy_efficiency_rankings': []
        }
        
        # Get scores for all cryptos
        all_scores = []
        consensus_groups = {}
        
        for crypto_id in self.crypto_profiles.keys():
            score_data = self.calculate_sustainability_score(crypto_id)
            all_scores.append(score_data)
            
            # Group by consensus mechanism
            consensus = score_data['consensus_mechanism']
            if consensus not in consensus_groups:
                consensus_groups[consensus] = []
            consensus_groups[consensus].append(score_data)
        
        # Sort and get top sustainable cryptos
        all_scores.sort(key=lambda x: x['total_score'], reverse=True)
        report['top_sustainable_cryptos'] = all_scores[:5]
        
        # Consensus analysis
        for consensus, cryptos in consensus_groups.items():
            avg_score = np.mean([crypto['total_score'] for crypto in cryptos])
            report['consensus_analysis'][consensus] = {
                'average_score': round(avg_score, 1),
                'count': len(cryptos),
                'cryptos': [crypto['name'] for crypto in cryptos]
            }
        
        # Energy efficiency rankings
        energy_sorted = sorted(all_scores, key=lambda x: x['energy_efficiency'], reverse=True)
        report['energy_efficiency_rankings'] = energy_sorted[:10]
        
        return report
