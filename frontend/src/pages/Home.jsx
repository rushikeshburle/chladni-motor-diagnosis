import React from 'react'
import { Link } from 'react-router-dom'
import { Activity, Upload, FileText, BarChart3, Shield, Zap, ArrowRight, Cpu, Waves } from 'lucide-react'

function Home() {
  return (
    <div className="space-y-12 animate-slide-up">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-3xl p-12 md:p-16 bg-gradient-to-r from-[#071A2B] via-[#0B1F3A] to-[#102A43]">
        <div className="relative z-10 max-w-4xl">
          <div className="flex items-center space-x-3 mb-6">
            <Waves className="w-8 h-8 text-[#06B6D4] animate-pulse" />
            <span className="text-sm font-medium text-[#06B6D4] uppercase tracking-wider">AI-Powered Motor Diagnosis</span>
          </div>
          <h1 className="text-5xl md:text-6xl font-bold font-heading mb-6 text-white leading-tight">
            VISION-BASED
          </h1>
          <h2 className="text-4xl md:text-5xl font-bold font-heading mb-6 gradient-text leading-tight">
            Chladni Pattern Analysis
          </h2>
          <p className="text-xl text-gray-300 mb-4 leading-relaxed">
            for Electric Motor Vibration Fault Diagnosis
          </p>
          <p className="text-gray-400 mb-10 text-lg leading-relaxed max-w-2xl">
            Analyze vibration patterns from images and videos to identify abnormal motor conditions using computer vision and machine learning.
          </p>
          <div className="flex flex-wrap gap-4">
            <Link to="/diagnosis" className="group btn-primary flex items-center space-x-2">
              <span>Start Diagnosis</span>
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link to="/history" className="btn-secondary">
              Explore System
            </Link>
          </div>
        </div>
        
        {/* Vibration Animation */}
        <div className="absolute right-10 top-1/2 transform -translate-y-1/2 hidden lg:block">
          <div className="relative w-64 h-64">
            {/* Rotating rings */}
            <div className="absolute inset-0 border-2 border-[#06B6D4]/30 rounded-full animate-spin" style={{ animationDuration: '8s' }} />
            <div className="absolute inset-4 border-2 border-[#2563EB]/30 rounded-full animate-spin" style={{ animationDuration: '6s', animationDirection: 'reverse' }} />
            <div className="absolute inset-8 border-2 border-[#06B6D4]/20 rounded-full animate-spin" style={{ animationDuration: '4s' }} />
            
            {/* Center motor icon */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-20 h-20 bg-gradient-to-br from-[#2563EB] to-[#06B6D4] rounded-full flex items-center justify-center animate-pulse-glow">
                <Cpu className="w-10 h-10 text-white" />
              </div>
            </div>
            
            {/* Pulsating waves */}
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-32 h-32 border border-[#06B6D4]/20 rounded-full animate-ping" style={{ animationDuration: '2s' }} />
            </div>
          </div>
        </div>
      </div>

      {/* Dashboard Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { icon: BarChart3, title: "Total Analyses", value: "1,284", color: "text-[#2563EB]" },
          { icon: Shield, title: "Faults Detected", value: "367", color: "text-[#EF4444]" },
          { icon: Activity, title: "Healthy Motors", value: "917", color: "text-[#22C55E]" },
          { icon: Cpu, title: "Model Accuracy", value: "96.8%", color: "text-[#06B6D4]" }
        ].map((stat, index) => (
          <div key={index} className="card hover:scale-105 hover:shadow-xl transition-all duration-300 cursor-pointer group">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-xl bg-[#F5F8FC] flex items-center justify-center group-hover:bg-[#2563EB]/10 transition-colors">
                <stat.icon className={`w-6 h-6 ${stat.color}`} />
              </div>
              <div className="w-2 h-2 bg-[#22C55E] rounded-full animate-pulse" />
            </div>
            <div className="text-3xl font-bold font-heading font-mono text-[#0F172A] mb-2">{stat.value}</div>
            <div className="text-sm text-gray-500">{stat.title}</div>
          </div>
        ))}
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          { icon: Upload, title: "Multimodal Input", desc: "Upload images, videos, and text descriptions" },
          { icon: Activity, title: "Pattern Analysis", desc: "Advanced Chladni pattern detection" },
          { icon: BarChart3, title: "Fault Classification", desc: "AI-powered classification of 8 fault types" },
          { icon: Shield, title: "Severity Assessment", desc: "Automatic severity with confidence scores" },
          { icon: Zap, title: "Explainable AI", desc: "Visual heatmaps and feature importance" },
          { icon: FileText, title: "PDF Reports", desc: "Professional diagnostic reports" }
        ].map((feature, index) => (
          <FeatureCard key={index} {...feature} index={index} />
        ))}
      </div>

      {/* Fault Classes Section */}
      <div className="card">
        <h2 className="text-3xl font-bold font-heading mb-8 gradient-text">Supported Fault Classes</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            "Healthy Motor",
            "Rotor Unbalance",
            "Shaft Misalignment",
            "Bearing Fault",
            "Rotor Fault",
            "Stator Fault",
            "Mechanical Looseness",
            "Coupling Fault"
          ].map((fault, index) => (
            <div key={fault} className="glass-card p-4 text-center hover:bg-[#2563EB]/10 hover:border-[#2563EB]/30 transition-all duration-300 hover:scale-105 cursor-pointer group">
              <span className="text-sm font-medium text-gray-600 group-hover:text-[#2563EB] transition-colors">{fault}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Workflow Section */}
      <div className="card">
        <h2 className="text-3xl font-bold font-heading mb-8 gradient-text">Diagnosis Workflow</h2>
        <div className="flex flex-wrap items-center justify-center gap-3">
          {[
            "Upload Input",
            "Preprocess",
            "Pattern Detection",
            "Feature Extraction",
            "Multimodal Fusion",
            "Classification",
            "Severity Assessment",
            "Report Generation"
          ].map((step, index) => (
            <React.Fragment key={step}>
              <div className="bg-[#F5F8FC] text-[#0F172A] px-4 py-2.5 rounded-xl font-medium text-sm border border-gray-200 hover:border-[#06B6D4]/50 hover:bg-[#06B6D4]/10 transition-all duration-300">
                {step}
              </div>
              {index < 7 && <div className="text-[#2563EB] text-lg">→</div>}
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  )
}

function FeatureCard({ icon: Icon, title, desc, index }) {
  return (
    <div className="card hover:scale-105 hover:shadow-xl transition-all duration-300 group cursor-pointer animate-slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
      <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-[#2563EB]/10 to-[#06B6D4]/10 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300 border border-[#06B6D4]/20">
        <Icon className="w-7 h-7 text-[#2563EB]" />
      </div>
      <h3 className="font-bold text-lg font-heading mb-2 text-[#0F172A]">{title}</h3>
      <p className="text-sm text-gray-500">{desc}</p>
    </div>
  )
}

export default Home
