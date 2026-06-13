import { eq, desc, count, sql } from "drizzle-orm";
import { getDb } from "./connection";
import { deals, type InsertDeal } from "@db/schema";

export async function findDeals(filter?: { stage?: string; type?: string }) {
  const db = getDb();
  const conditions: Array<ReturnType<typeof sql>> = [];
  
  if (filter?.stage) conditions.push(sql`${deals.stage} = ${filter.stage}`);
  if (filter?.type) conditions.push(sql`${deals.type} = ${filter.type}`);
  
  if (conditions.length > 0) {
    return db.select().from(deals).where(conditions[0]).orderBy(desc(deals.createdAt));
  }
  return db.select().from(deals).orderBy(desc(deals.createdAt));
}

export async function findDealById(id: number) {
  const db = getDb();
  const results = await db.select().from(deals).where(eq(deals.id, id)).limit(1);
  return results[0] ?? null;
}

export async function createDeal(data: InsertDeal) {
  const db = getDb();
  const result = await db.insert(deals).values(data);
  return { id: Number(result[0].insertId) };
}

export async function updateDeal(id: number, data: Partial<InsertDeal>) {
  const db = getDb();
  await db.update(deals).set(data).where(eq(deals.id, id));
  return findDealById(id);
}

export async function deleteDeal(id: number) {
  const db = getDb();
  await db.delete(deals).where(eq(deals.id, id));
  return { success: true };
}

export async function getDealStats() {
  const db = getDb();
  const total = await db.select({ count: count() }).from(deals);
  const byStage = await db
    .select({ stage: deals.stage, count: count(), value: sql<number>`COALESCE(SUM(${deals.value}), 0)` })
    .from(deals)
    .groupBy(deals.stage);
  const totalValue = await db.select({ total: sql<number>`COALESCE(SUM(${deals.value}), 0)` }).from(deals);
  const weightedValue = await db
    .select({ weighted: sql<number>`COALESCE(SUM(${deals.value} * ${deals.probability} / 100), 0)` })
    .from(deals);
  return {
    total: total[0]?.count ?? 0,
    byStage,
    totalValue: totalValue[0]?.total ?? 0,
    weightedValue: weightedValue[0]?.weighted ?? 0,
  };
}
