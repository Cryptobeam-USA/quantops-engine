require('dotenv').config();
const fastify = require('fastify')({ logger: process.env.LOG_LEVEL || false });

const service = {
  name: 'QuantOps Engine',
  repo: 'quantops-engine',
  summary: 'Backtesting, live trading hooks, and risk controls.',
  owners: ['backend', 'platform', 'security'],
};

function health() {
  return {
    service: service.name,
    status: 'ok',
    timestamp: new Date().toISOString(),
  };
}

function planWorkflow(input) {
  const steps = [
    'validate inputs',
    'load configuration',
    'execute core workflow',
    'emit telemetry',
  ];
  return {
    id: input.id || 'draft',
    steps,
    notes: `preview for ${input.useCase || 'baseline'}`,
  };
}

fastify.get('/health', async () => health());
fastify.post('/plan', async (request) => planWorkflow(request.body || {}));

if (require.main === module) {
  if (process.argv.includes('--self-test')) {
    console.log('[health]', health());
    console.log('[plan]', planWorkflow({ useCase: 'sandbox' }));
    process.exit(0);
  }
  const port = process.env.PORT || 3000;
  fastify.listen({ port, host: '0.0.0.0' }).then(() => {
    console.log(`Service ${service.name} listening on ${port}`);
  }).catch((err) => {
    console.error(err);
    process.exit(1);
  });
}

module.exports = { service, health, planWorkflow };
