import { eq, desc, count, sql, like } from "drizzle-orm";
import { getDb } from "./connection";
import { prospects, type InsertProspect } from "@db/schema";

export async function findProspects(filter?: { segment?: string; status?: string; search?: string }) {
  const db = getDb();
  if (filter?.segment) {
    return db.select().from(prospects).where(sql`${prospects.segment} = ${filter.segment}`).orderBy(desc(prospects.createdAt));
  }
  if (filter?.status) {
    return db.select().from(prospects).where(sql`${prospects.status} = ${filter.status}`).orderBy(desc(prospects.createdAt));
  }
  if (filter?.search) {
    return db.select().from(prospects).where(like(prospects.company, `%${filter.search}%`)).orderBy(desc(prospects.createdAt));
  }
  return db.select().from(prospects).orderBy(desc(prospects.createdAt));
}

export async function findProspectById(id: number) {
  const db = getDb();
  const results = await db.select().from(prospects).where(eq(prospects.id, id)).limit(1);
  return results[0] ?? null;
}

export async function createProspect(data: InsertProspect) {
  const db = getDb();
  const result = await db.insert(prospects).values(data);
  return { id: Number(result[0].insertId) };
}

export async function updateProspect(id: number, data: Partial<InsertProspect>) {
  const db = getDb();
  await db.update(prospects).set(data).where(eq(prospects.id, id));
  return findProspectById(id);
}

export async function deleteProspect(id: number) {
  const db = getDb();
  await db.delete(prospects).where(eq(prospects.id, id));
  return { success: true };
}

export async function getProspectStats() {
  const db = getDb();
  const total = await db.select({ count: count() }).from(prospects);
  const byStatus = await db
    .select({ status: prospects.status, count: count() })
    .from(prospects)
    .groupBy(prospects.status);
  const bySegment = await db
    .select({ segment: prospects.segment, count: count() })
    .from(prospects)
    .groupBy(prospects.segment);
  const totalValue = await db
    .select({ total: sql<number>`COALESCE(SUM(${prospects.value}), 0)` })
    .from(prospects);
  return {
    total: total[0]?.count ?? 0,
    byStatus,
    bySegment,
    totalValue: totalValue[0]?.total ?? 0,
  };
}
