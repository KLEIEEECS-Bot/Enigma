from flask import Flask, render_template, request, jsonify
import re
import json
from datetime import datetime

app = Flask(__name__)

class CyberattackAnalyzer:
    def __init__(self):
        # Enhanced keyword-based attack detection with user-friendly explanations
        self.attack_patterns = {
            'phishing': {
                'keywords': [
                    # Email-related phishing terms
                    'phishing', 'fake email', 'suspicious email', 'fraudulent email', 'scam email',
                    'email scam', 'spoofed email', 'malicious email', 'deceptive email',
                    
                    # Link and website terms
                    'suspicious link', 'malicious link', 'fake link', 'click here', 'click link',
                    'fake website', 'spoofed website', 'malicious website', 'fraudulent site',
                    'fake site', 'lookalike website', 'imposter site',
                    
                    # Credential stealing terms
                    'steal password', 'steal login', 'steal credentials', 'harvest credentials',
                    'password theft', 'credential theft', 'login theft', 'account theft',
                    'phish credentials', 'capture password', 'steal banking info',
                    
                    # Authentication terms
                    'verify account', 'confirm account', 'validate account', 'update account',
                    'secure account', 'protect account', 'account verification', 'login verification',
                    'two-factor', '2fa', 'authentication', 'account suspended', 'account locked',
                    
                    # Banking and financial terms
                    'bank account', 'banking details', 'account details', 'financial information',
                    'credit card', 'debit card', 'card details', 'payment information',
                    'online banking', 'bank login', 'account balance', 'transaction',
                    
                    # Urgency and pressure terms
                    'urgent action', 'immediate action', 'act now', 'limited time', 'expires soon',
                    'account will be closed', 'suspended account', 'security breach', 'compromised account',
                    
                    # Impersonation terms
                    'trusted bank', 'legitimate company', 'official email', 'security team',
                    'customer service', 'support team', 'account team', 'fraud department'
                ],
                'simple_name': 'Email Trick (Phishing)',
                'simple_explanation': "This is like someone pretending to be your friend to get into your house, but they do it through email to steal your money.",
                'real_example': "You get an email that looks like it's from your bank saying 'Your account will be closed! Click here now!' But it's actually from a criminal trying to steal your password.",
                'story_template': "Someone tried to trick you by sending a fake email that looks real. They wanted you to click on a dangerous link or give them your password so they could steal your money or personal information.",
                'warning_signs': [
                    "The email asks you to 'click here urgently'",
                    "It threatens to close your account if you don't act fast",
                    "It asks for your password or bank details",
                    "The sender's email address looks strange or different"
                ],
                'actions': [
                    "Never click links in suspicious emails - instead, go directly to your bank's website by typing it yourself",
                    "Never give your password to anyone via email - real banks never ask for this",
                    "Banks never ask for passwords in emails - if unsure, call your bank using the number on your card",
                    "Delete suspicious emails immediately and don't reply to them",
                    "Check your bank account regularly to make sure no money is missing"
                ]
            },
            'social_engineering': {
                'keywords': [
                    # Communication methods
                    'phone call', 'cold call', 'unsolicited call', 'robocall', 'telemarketing',
                    'text message', 'sms', 'instant message', 'chat message', 'social media message',
                    
                    # Impersonation terms
                    'tech support', 'technical support', 'customer support', 'help desk',
                    'microsoft', 'apple', 'google', 'facebook', 'amazon', 'paypal',
                    'irs', 'social security', 'medicare', 'government agency', 'police',
                    'bank representative', 'insurance agent', 'utility company',
                    
                    # Tactics and manipulation
                    'social engineering', 'manipulation', 'pressure tactics', 'fear tactics',
                    'urgency', 'emergency', 'immediate action required', 'time sensitive',
                    'limited offer', 'special deal', 'exclusive offer', 'one-time opportunity',
                    
                    # Requests for access/information
                    'remote access', 'screen sharing', 'teamviewer', 'anydesk', 'remote desktop',
                    'install software', 'download program', 'grant permission', 'give access',
                    'personal information', 'sensitive information', 'confidential data',
                    
                    # Payment and financial requests
                    'gift card', 'itunes card', 'google play card', 'prepaid card', 'money transfer',
                    'wire transfer', 'western union', 'moneygram', 'bitcoin', 'cryptocurrency',
                    'refund', 'overpayment', 'tax refund', 'stimulus check', 'lottery winnings'
                ],
                'simple_name': 'Phone/Text Trick (Social Engineering)',
                'simple_explanation': "This is like a stranger calling you pretending to be your grandson in trouble, but they want money or access to your computer.",
                'real_example': "Someone calls saying 'Hi, this is Microsoft tech support. Your computer has a virus and we need remote access to fix it right now!' But Microsoft never calls people like this.",
                'story_template': "Someone contacted you (by phone, email, or message) pretending to be from a trusted company or government agency. They tried to trick you into giving them personal information, money, or access to your computer.",
                'warning_signs': [
                    "They called you out of nowhere claiming there's an urgent problem",
                    "They ask for remote access to your computer",
                    "They want payment with gift cards or wire transfers",
                    "They pressure you to act immediately without time to think"
                ],
                'actions': [
                    "Hang up immediately on any suspicious calls - you can always call them back",
                    "Never give personal information to people who call you first",
                    "Real companies never ask for passwords over the phone",
                    "Never let strangers control your computer remotely",
                    "Never pay anyone with gift cards - this is always a scam",
                    "When in doubt, hang up and call a family member or the company directly",
                    "Take time to think - real emergencies don't require gift card payments"
                ]
            },
            'malware': {
                'keywords': [
                    # Malware types and symptoms  
                    'malware', 'virus', 'trojan', 'ransomware', 'spyware', 'adware', 'worm',
                    'computer slow', 'system slow', 'popup ads', 'unwanted ads', 'browser hijack',
                    'homepage changed', 'new toolbar', 'unexpected programs', 'files encrypted',
                    'download', 'install', 'suspicious download', 'free download', 'attachment',
                    'infected', 'suspicious website', 'untrusted source', 'executable',
                    'slow performance', 'frequent crashes', 'system freeze'
                ],
                'simple_name': 'Computer Infection (Malware)',
                'simple_explanation': "This is like germs getting into your computer and making it sick. Your computer becomes slow and shows strange things.",
                'real_example': "You downloaded a 'free' program to make your computer faster, but now your computer is actually slower and shows lots of popup ads everywhere.",
                'story_template': "Bad software (called malware) got into your computer and is causing problems. This usually happens when you download something dangerous from the internet or open a bad email attachment.",
                'warning_signs': [
                    "Your computer is suddenly much slower than usual",
                    "You see popup ads everywhere, even when not browsing",
                    "Your homepage changed to something you didn't set",
                    "Programs you didn't install are now on your computer"
                ],
                'actions': [
                    "Don't download 'free' programs from websites you don't trust",
                    "Don't open email attachments from people you don't know well",
                    "If your computer is acting strange, ask a tech-savvy family member for help",
                    "Keep your computer updated with the latest security patches",
                    "Use antivirus software and let it scan your computer regularly"
                ]
            },
            'identity_theft': {
                'keywords': [
                    'identity theft', 'personal information', 'social security number', 'ssn',
                    'credit card', 'bank account', 'drivers license', 'stolen wallet',
                    'unauthorized charges', 'unknown accounts', 'credit report', 'fraud alert',
                    'data breach', 'personal data', 'financial information', 'account credentials'
                ],
                'simple_name': 'Identity Stealing',
                'simple_explanation': "This is like someone stealing your wallet and pretending to be you to spend your money or open accounts in your name.",
                'real_example': "You notice charges on your credit card for things you never bought, or you get bills for accounts you never opened. Someone stole your information and is pretending to be you.",
                'story_template': "Someone stole your personal information (like your social security number or credit card details) and is using it to pretend they are you, potentially opening accounts or making purchases in your name.",
                'warning_signs': [
                    "Charges on your credit card or bank account that you didn't make",
                    "Bills or accounts you never opened arriving in your name", 
                    "Your credit report shows accounts or inquiries you didn't authorize",
                    "You stop receiving expected mail or bills"
                ],
                'actions': [
                    "Check all your bank and credit card statements right away",
                    "Call your bank and credit card companies immediately to report the problem",
                    "Ask them to put a fraud alert on your accounts",
                    "Consider 'freezing' your credit so no new accounts can be opened",
                    "Keep checking your accounts regularly for anything suspicious",
                    "Keep records of all your phone calls and actions"
                ]
            },
            'ransomware': {
                'keywords': [
                    'ransomware', 'ransom', 'encrypted files', 'locked files', 'files encrypted',
                    'cannot open files', 'files corrupted', 'ransom note', 'payment demand',
                    'bitcoin payment', 'cryptocurrency', 'decrypt files', 'unlock files'
                ],
                'simple_name': 'File Kidnapping (Ransomware)',
                'simple_explanation': "This is like criminals breaking into your house and locking all your photo albums in a safe, then demanding money to give you the key.",
                'real_example': "You try to open your family photos or important documents, but they won't open. Instead, you see a message saying 'Pay $500 in Bitcoin to get your files back.'",
                'story_template': "Criminals have locked up all your important files on your computer and are demanding money to unlock them. This is like digital kidnapping of your photos and documents.",
                'warning_signs': [
                    "You can't open any of your photos, documents, or files",
                    "File names look strange or have different endings",
                    "A message appears demanding money to unlock your files",
                    "Your desktop background changed to a ransom message"
                ],
                'actions': [
                    "DO NOT pay the money - there's no guarantee you'll get your files back",
                    "Disconnect your computer from the internet right away",
                    "Don't turn your computer off and on again unless an expert tells you to",
                    "Call a computer expert or tech-savvy family member immediately",
                    "Report this crime to your local police",
                    "Check if you have backup copies of your files somewhere else"
                ]
            }
        }
    
    def detect_attack_type(self, description):
        description_lower = description.lower()
        scores = {}
        
        # Calculate weighted scores for each attack type
        for attack_type, data in self.attack_patterns.items():
            score = 0
            matched_keywords = []
            
            for keyword in data['keywords']:
                if keyword in description_lower:
                    # Weight longer, more specific keywords higher
                    keyword_weight = len(keyword.split()) * 1.5 if len(keyword.split()) > 1 else 1
                    score += keyword_weight
                    matched_keywords.append(keyword)
            
            # Bonus for multiple keyword matches
            if len(matched_keywords) > 3:
                score *= 1.2
            
            scores[attack_type] = {
                'score': score,
                'matched_keywords': matched_keywords,
                'match_count': len(matched_keywords)
            }
        
        # Find the best match
        best_attack = max(scores, key=lambda x: scores[x]['score'])
        best_score = scores[best_attack]['score']
        
        # Return unknown if confidence is too low
        if best_score < 2:  # Require at least 2 points of confidence
            return 'unknown'
        
        return best_attack
    
    def get_detection_confidence(self, attack_type, description):
        """Get confidence level and matched keywords for debugging"""
        if attack_type == 'unknown':
            return {'confidence': 'low', 'matched_keywords': []}
        
        description_lower = description.lower()
        matched_keywords = []
        
        for keyword in self.attack_patterns[attack_type]['keywords']:
            if keyword in description_lower:
                matched_keywords.append(keyword)
        
        confidence_level = 'low'
        if len(matched_keywords) >= 5:
            confidence_level = 'high'
        elif len(matched_keywords) >= 3:
            confidence_level = 'medium'
        
        return {
            'confidence': confidence_level,
            'matched_keywords': matched_keywords,
            'total_matches': len(matched_keywords)
        }
    
    def generate_story(self, attack_type, original_description):
        if attack_type == 'unknown':
            return "We detected some suspicious computer activity, but we're not sure exactly what type. The important thing is to stay safe online."
        
        return self.attack_patterns[attack_type]['story_template']
    
    def generate_actions(self, attack_type):
        if attack_type == 'unknown':
            return [
                "Don't panic - you're taking the right steps",
                "Don't click on suspicious links or downloads",
                "Ask a tech-savvy family member for help",
                "Consider calling your bank if money might be involved"
            ]
        
        return self.attack_patterns[attack_type]['actions']

analyzer = CyberattackAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_attack():
    try:
        data = request.get_json()
        description = data.get('description', '')
        
        if not description:
            return jsonify({'error': 'No description provided'}), 400
        
        # Analyze the attack
        attack_type = analyzer.detect_attack_type(description)
        story = analyzer.generate_story(attack_type, description)
        actions = analyzer.generate_actions(attack_type)
        confidence_info = analyzer.get_detection_confidence(attack_type, description)
        
        result = {
            'attack_type': attack_type.replace('_', ' ').title(),
            'story': story,
            'actions': actions,
            'confidence': confidence_info['confidence'],
            'matched_keywords': confidence_info.get('matched_keywords', [])[:10],  # Show max 10 keywords
            'total_matches': confidence_info.get('total_matches', 0),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)