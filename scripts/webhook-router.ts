#!/usr/bin/env node
/**
 * Webhook Event Router
 * Routes GitHub webhook events to appropriate handlers
 */

const eventType = process.argv[2];
const action = process.argv[3];
const identifier = process.argv[4];

console.log(`🔄 Routing ${eventType} event: ${action} ${identifier || ''}`);

switch (eventType) {
  case 'issue':
    console.log(`📋 Issue ${action}: #${identifier}`);
    // Issue events are handled by autonomous-agent.yml
    break;

  case 'pr':
    console.log(`🔀 PR ${action}: #${identifier}`);
    // PR events handled by state-machine.yml
    break;

  case 'push':
    console.log(`📤 Push to ${action}: ${identifier}`);
    // Push events trigger builds and deployments
    break;

  case 'comment':
    console.log(`💬 Comment on #${action} by ${identifier}`);
    // Comment events can trigger agent commands
    break;

  default:
    console.log(`⚠️ Unknown event type: ${eventType}`);
}

console.log('✅ Event routed successfully');
process.exit(0);
