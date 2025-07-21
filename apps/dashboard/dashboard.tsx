"use client"

import {
  CalendarDays,
  Download,
  ChevronDown,
  TrendingUp,
  AlertTriangle,
  Ship,
  Cpu,
  MessageSquare,
  Thermometer,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuCheckboxItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export default function TaiwanStraitDashboard() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-slate-900">
      {/* Header */}
      <header className="bg-slate-100 dark:bg-slate-800 border-b border-slate-300 dark:border-slate-600 px-6 py-4">
        <div className="max-w-screen-xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">Taiwan Strait Risk Dashboard</h1>

          <div className="flex items-center gap-3">
            {/* Date Range Picker */}
            <Button
              variant="outline"
              className="gap-2 bg-transparent border-slate-300 dark:border-slate-600 dark:text-slate-400"
            >
              <CalendarDays className="h-4 w-4" />
              Seleccionar fechas
            </Button>

            {/* Multi-select Dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="outline"
                  className="gap-2 bg-transparent border-slate-300 dark:border-slate-600 dark:text-slate-400"
                >
                  Indicadores
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56">
                <DropdownMenuCheckboxItem checked>TAIEX</DropdownMenuCheckboxItem>
                <DropdownMenuCheckboxItem checked>CDS Spreads</DropdownMenuCheckboxItem>
                <DropdownMenuCheckboxItem>VIX</DropdownMenuCheckboxItem>
                <DropdownMenuCheckboxItem checked>AIS Data</DropdownMenuCheckboxItem>
                <DropdownMenuCheckboxItem>SOX Index</DropdownMenuCheckboxItem>
                <DropdownMenuCheckboxItem>TSMC Exports</DropdownMenuCheckboxItem>
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Export Button */}
            <Button className="gap-2">
              <Download className="h-4 w-4" />
              Exportar CSV
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6 space-y-6">
        {/* Row 1: 3 Equal Cards */}
        <div className="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <Card className="dark:bg-slate-800 border-slate-300 dark:border-slate-600 overflow-hidden">
            <CardHeader>
              <CardTitle className="text-lg dark:text-slate-100">
                <TrendingUp className="inline-block w-4 h-4 mr-2 text-slate-500 dark:text-slate-400" />
                Visión de mercado
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-auto">
                <div className="h-52 lg:h-[260px] bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center border-2 border-dashed border-slate-300 dark:border-slate-600">
                  <span className="text-slate-500 dark:text-slate-400 font-medium">Candlestick TAIEX</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="dark:bg-slate-800 border-slate-300 dark:border-slate-600 overflow-hidden">
            <CardHeader>
              <CardTitle className="text-lg dark:text-slate-100">
                <AlertTriangle className="inline-block w-4 h-4 mr-2 text-slate-500 dark:text-slate-400" />
                Riesgo financiero
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-auto">
                <div className="h-52 lg:h-[260px] bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center border-2 border-dashed border-slate-300 dark:border-slate-600">
                  <span className="text-slate-500 dark:text-slate-400 font-medium">Área spreads CDS & VIX</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="dark:bg-slate-800 border-slate-300 dark:border-slate-600 overflow-hidden">
            <CardHeader>
              <CardTitle className="text-lg dark:text-slate-100">
                <Ship className="inline-block w-4 h-4 mr-2 text-slate-500 dark:text-slate-400" />
                Comercio & cadena de suministro
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-auto">
                <div className="h-52 lg:h-[260px] bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center border-2 border-dashed border-slate-300 dark:border-slate-600">
                  <span className="text-slate-500 dark:text-slate-400 font-medium">Heatmap AIS</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Row 2: 2/3 and 1/3 Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          <Card className="lg:col-span-2 dark:bg-slate-800 border-slate-300 dark:border-slate-600 overflow-hidden">
            <CardHeader>
              <CardTitle className="text-lg dark:text-slate-100">
                <Cpu className="inline-block w-4 h-4 mr-2 text-slate-500 dark:text-slate-400" />
                Tecnología & semiconductores
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-auto">
                <div className="min-h-[340px] bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center border-2 border-dashed border-slate-300 dark:border-slate-600">
                  <span className="text-slate-500 dark:text-slate-400 font-medium text-base">
                    Línea SOX vs Nasdaq + barras export TSMC
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="dark:bg-slate-800 border-slate-300 dark:border-slate-600 overflow-hidden">
            <CardHeader>
              <CardTitle className="text-lg dark:text-slate-100">
                <MessageSquare className="inline-block w-4 h-4 mr-2 text-slate-500 dark:text-slate-400" />
                Sentimiento geopolítico
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-auto">
                <div className="h-[300px] bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center border-2 border-dashed border-slate-300 dark:border-slate-600">
                  <span className="text-slate-500 dark:text-slate-400 font-medium text-center">
                    Nube de palabras + score
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Row 3: Full Width Risk Thermometer */}
        <Card className="ring-2 ring-orange-200/60 dark:ring-orange-300/40 bg-orange-50 dark:bg-orange-950/20 border-slate-300 dark:border-slate-600 overflow-hidden">
          <CardHeader>
            <CardTitle className="text-lg text-center dark:text-slate-100">
              <Thermometer className="inline-block w-4 h-4 mr-2 text-slate-500 dark:text-slate-400" />
              Termómetro de riesgo
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-auto">
              <div className="h-[200px] bg-slate-100 dark:bg-slate-700 rounded-lg flex items-center justify-center border-2 border-dashed border-slate-300 dark:border-slate-600">
                <span className="text-slate-500 dark:text-slate-400 font-medium">Gauge 0-100</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
