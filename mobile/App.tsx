/**
 * Dealix mobile companion — Expo / React Native.
 *
 * Scope of this skeleton: read-only approvals view + status pill.
 * Push notifications + full deal CRUD land in v0.2.
 */

import { StatusBar } from "expo-status-bar";
import { useEffect, useState } from "react";
import { StyleSheet, Text, View } from "react-native";

const API_BASE = process.env.EXPO_PUBLIC_API_BASE ?? "https://api.dealix.me";

export default function App() {
  const [status, setStatus] = useState<string>("loading");
  const [version, setVersion] = useState<string>("");

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/status`)
      .then((r) => r.json())
      .then((data) => {
        setStatus(String(data?.status ?? "unknown"));
        setVersion(String(data?.version ?? ""));
      })
      .catch(() => setStatus("unreachable"));
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Dealix</Text>
      <Text style={[styles.pill, status === "ok" ? styles.ok : styles.warn]}>{status}</Text>
      <Text style={styles.meta}>v{version}</Text>
      <Text style={styles.help}>
        Open the dashboard at https://app.dealix.me for full access. This app is
        read-only in v0.1.
      </Text>
      <StatusBar style="light" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0a0e1a",
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
  },
  title: { color: "#fff", fontSize: 32, fontWeight: "700" },
  pill: {
    marginTop: 16,
    paddingHorizontal: 16,
    paddingVertical: 6,
    borderRadius: 999,
    fontWeight: "700",
  },
  ok: { backgroundColor: "rgba(74,222,128,0.15)", color: "#4ade80" },
  warn: { backgroundColor: "rgba(251,191,36,0.15)", color: "#fbbf24" },
  meta: { color: "#8a93a8", marginTop: 8 },
  help: { color: "#8a93a8", marginTop: 24, textAlign: "center" },
});
