import { Link } from 'react-router'
import { ArrowLeft } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { type SystemInfo, formatSar } from '@/data/systems'
import { systemMeta } from './systemMeta'

export default function SystemCard({ system }: { system: SystemInfo }) {
  const meta = systemMeta(system.id)
  const Icon = meta.icon
  return (
    <Link to={`/systems/${system.slug}`} className="block group">
      <Card className="h-full border-0 shadow-md hover:shadow-lg transition-shadow">
        <CardHeader>
          <div className="flex items-center justify-between mb-3">
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${meta.iconBg}`}>
              <Icon className="w-6 h-6" />
            </div>
            <Badge variant="outline">يبدأ من {formatSar(system.startingPriceSar)} ر.س</Badge>
          </div>
          <CardTitle className="text-xl">{system.nameAr}</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-600 leading-relaxed mb-4">{system.taglineAr}</p>
          <span className={`inline-flex items-center gap-1 text-sm font-medium ${meta.accentText}`}>
            التفاصيل
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
          </span>
        </CardContent>
      </Card>
    </Link>
  )
}
