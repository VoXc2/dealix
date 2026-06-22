import { Hono } from 'hono';
import { getDb } from './queries/connection';
import { sql } from 'drizzle-orm';

const health = new Hono();

health.get('/health', (c) => {
  return c.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: process.env.npm_package_version || '1.0.0',
    environment: process.env.NODE_ENV || 'development',
    uptime: process.uptime(),
    memory: process.memoryUsage(),
  });
});

health.get('/ready', async (c) => {
  try {
    // Check database connectivity
    const db = getDb();
    await db.execute(sql`SELECT 1`);
    
    return c.json({
      status: 'ready',
      checks: {
        database: 'connected',
        application: 'running',
      },
      timestamp: new Date().toISOString(),
    });
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    return c.json({
      status: 'not_ready',
      checks: {
        database: 'disconnected',
        application: 'running',
      },
      error: errorMessage,
      timestamp: new Date().toISOString(),
    }, 503);
  }
});

export default health;
