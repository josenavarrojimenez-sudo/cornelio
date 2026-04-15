#!/usr/bin/env python3
"""
Register remaining agents in Paperclip
Cleo, Prolix, Abaco, Flavia
"""

import requests
import json
import sys

# Configuración
PAPERCLIP_URL = "http://31.97.214.129:65158"
COMPANY_ID = "44a2bc4e-bfce-420a-ba86-bf3424f43366"

# Credenciales de admin
ADMIN_EMAIL = "jose.navarro.jimenez@gmail.com"
ADMIN_PASSWORD = "yIoUqn9wp1ezBDbeBHQPCxECfG60uNtt"

def get_auth_token():
    """Login to Paperclip"""
    session = requests.Session()
    response = session.post(
        f"{PAPERCLIP_URL}/api/auth/sign-in/email",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    
    if response.status_code == 200:
        print("✅ Authentication successful")
        return session
    else:
        print(f"❌ Auth failed: {response.status_code}")
        return None

def get_cornelio_id(session):
    """Get Cornelio's agent ID"""
    # Buscar en los archivos locales primero
    try:
        with open("/root/.openclaw/workspace/paperclip_claimed_api_key.json") as f:
            data = json.load(f)
            if data.get('agentId'):
                return data['agentId']
    except:
        pass
    
    # Intentar via API
    response = session.get(f"{PAPERCLIP_URL}/api/companies/{COMPANY_ID}/agents")
    if response.status_code == 200:
        agents = response.json()
        if isinstance(agents, list):
            for agent in agents:
                if agent.get('name') == 'Cornelio':
                    return agent.get('id')
    return None

def create_agent(session, agent_data):
    """Create agent in Paperclip"""
    response = session.post(
        f"{PAPERCLIP_URL}/api/companies/{COMPANY_ID}/agents",
        json=agent_data
    )
    
    if response.status_code == 200:
        agent = response.json()
        print(f"✅ Created: {agent.get('name')} ({agent.get('id')})")
        return agent
    else:
        print(f"❌ Failed: {response.status_code} - {response.text[:200]}")
        return None

def generate_api_key(session, agent_id):
    """Generate API key"""
    response = session.post(f"{PAPERCLIP_URL}/api/agents/{agent_id}/keys")
    if response.status_code == 200:
        return response.json().get('key')
    return None

def update_reports_to(session, agent_id, reports_to_id):
    """Update reporting structure"""
    response = session.patch(
        f"{PAPERCLIP_URL}/api/agents/{agent_id}",
        json={"reportsTo": reports_to_id}
    )
    return response.status_code == 200

def main():
    print("=" * 60)
    print("📋 Registering Remaining Agents in Paperclip")
    print("=" * 60)
    
    # Authenticate
    session = get_auth_token()
    if not session:
        return 1
    
    # Get Cornelio ID
    cornelio_id = get_cornelio_id(session)
    if not cornelio_id:
        print("❌ Could not find Cornelio")
        return 1
    print(f"✅ Found Cornelio: {cornelio_id}")
    
    # Agents to register
    agents = [
        {
            "name": "Cleo",
            "role": "specialist",
            "title": "Especialista Frontend",
            "reportsTo": cornelio_id,
            "capabilities": "Desarrollo frontend, UI/UX, HTML/CSS/JavaScript, frameworks web",
            "status": "running",
            "adapterType": "http",
            "adapterConfig": {"url": "http://localhost:8080/webhook/cleo", "timeoutSec": 300}
        },
        {
            "name": "Prolix",
            "role": "specialist",
            "title": "Agente de Investigación",
            "reportsTo": cornelio_id,
            "capabilities": "Investigación web, scraping, análisis de datos, reportes",
            "status": "running",
            "adapterType": "http",
            "adapterConfig": {"url": "http://localhost:8080/webhook/prolix", "timeoutSec": 300}
        },
        {
            "name": "Abaco",
            "role": "specialist",
            "title": "Especialista Presupuestos Inmobiliarios",
            "reportsTo": cornelio_id,
            "capabilities": "Presupuestos, análisis inmobiliario, costos de construcción",
            "status": "running",
            "adapterType": "http",
            "adapterConfig": {"url": "http://localhost:8080/webhook/abaco", "timeoutSec": 300}
        },
        {
            "name": "Flavia",
            "role": "specialist",
            "title": "Especialista Marketing",
            "reportsTo": cornelio_id,
            "capabilities": "Marketing digital, Meta Ads, análisis de campañas, estrategia",
            "status": "running",
            "adapterType": "http",
            "adapterConfig": {"url": "http://localhost:8080/webhook/flavia", "timeoutSec": 300}
        }
    ]
    
    created_agents = []
    
    for agent_data in agents:
        print(f"\n📝 Creating {agent_data['name']}...")
        agent = create_agent(session, agent_data)
        if agent:
            api_key = generate_api_key(session, agent['id'])
            if api_key:
                print(f"   🔑 API Key: {api_key[:20]}...")
                agent['apiKey'] = api_key
            created_agents.append(agent)
    
    # Save to file
    output = {
        "companyId": COMPANY_ID,
        "registeredAt": "2026-04-15T17:55:00Z",
        "agents": created_agents
    }
    
    with open("/root/.openclaw/workspace/paperclip_remaining_agents.json", 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "=" * 60)
    print("✅ Registration Complete!")
    print("=" * 60)
    for agent in created_agents:
        print(f"\n👤 {agent['name']} ({agent['title']})")
        print(f"   ID: {agent['id']}")
        print(f"   API Key: {agent.get('apiKey', 'N/A')[:20]}...")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
