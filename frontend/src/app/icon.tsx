import { ImageResponse } from "next/og";

export const size = { width: 32, height: 32 };
export const contentType = "image/png";
export const runtime = "edge";

export default function Icon() {
  return new ImageResponse(
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "#0c2742",
        borderRadius: 8,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Diamond accent */}
      <div
        style={{
          position: "absolute",
          width: 20,
          height: 20,
          border: "1.5px solid #d4a843",
          transform: "rotate(45deg)",
          borderRadius: 2,
          opacity: 0.2,
        }}
      />
      <span style={{ color: "#d4a843", fontSize: 18, fontWeight: 700, fontFamily: "Inter, sans-serif" }}>
        D
      </span>
    </div>,
    { ...size }
  );
}
