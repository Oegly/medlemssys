# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'LokallagStat.lokallag'
        db.alter_column(u'statistikk_lokallagstat', 'lokallag_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['medlem.Lokallag'], null=True, on_delete=models.SET_NULL))

    def backwards(self, orm):

        # Changing field 'LokallagStat.lokallag'
        db.alter_column(u'statistikk_lokallagstat', 'lokallag_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['medlem.Lokallag']))

    models = {
        u'medlem.lokallag': {
            'Meta': {'ordering': "['-aktivt', 'namn']", 'object_name': 'Lokallag'},
            'aktivt': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'andsvar': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'distrikt': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'epost': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'fylkeslag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lokalsats': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'namn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'})
        },
        u'statistikk.lokallagstat': {
            'Meta': {'unique_together': "(('lokallag', 'veke'),)", 'object_name': 'LokallagStat'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interessante': ('django.db.models.fields.TextField', [], {}),
            'lokallag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['medlem.Lokallag']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'n_ikkje_utmelde': ('django.db.models.fields.IntegerField', [], {}),
            'n_interessante': ('django.db.models.fields.IntegerField', [], {}),
            'n_teljande': ('django.db.models.fields.IntegerField', [], {}),
            'n_totalt': ('django.db.models.fields.IntegerField', [], {}),
            'oppretta': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'teljande': ('django.db.models.fields.TextField', [], {}),
            'veke': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        }
    }

    complete_apps = ['statistikk']