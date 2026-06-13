import { eq, desc, count, sql } from "drizzle-orm";
import { getDb } from "./connection";
import { activities, type InsertActivity } from "@db/schema";

export async function findActivities(filter?: { prospectId?: number; type?: string }) {
  const db = getDb();
  if (filter?.prospectId) {
    return db.select().from(activities).where(eq(activities.prospectId, filter.prospectId)).orderBy(desc(activities.createdAt));
  }
  if (filter?.type) {
    return db.select().from(activities).where(sql`${activities.type} = ${filter.type}`).orderBy(desc(activities.createdAt));
  }
  return db.select().from(activities).orderBy(desc(activities.createdAt));
}

export async function createActivity(data: InsertActivity) {
  const db = getDb();
  const result = await db.insert(activities).values(data);
  return { id: Number(result[0].insertId) };
}

export async function updateActivity(id: number, data: Partial<InsertActivity>) {
  const db = getDb();
  await db.update(activities).set(data).where(eq(activities.id, id));
  return db.select().from(activities).where(eq(activities.id, id)).limit(1).then(r => r[0] ?? null);
}

export async function deleteActivity(id: number) {
  const db = getDb();
  await db.delete(activities).where(eq(activities.id, id));
  return { success: true };
}

export async function getActivityStats() {
  const db = getDb();
  const total = await db.select({ count: count() }).from(activities);
  const byType = await db
    .select({ type: activities.type, count: count() })
    .from(activities)
    .groupBy(activities.type);
  const byStatus = await db
    .select({ status: activities.status, count: count() })
    .from(activities)
    .groupBy(activities.status);
  return {
    total: total[0]?.count ?? 0,
    byType,
    byStatus,
  };
}
