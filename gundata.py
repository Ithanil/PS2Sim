import csv
#from numpy import *
#import matplotlib as plt
from pylab import *
from numpy.random import *
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

def rand_unicirc():
	t = 2*pi*random()
	u = random()+random()
	if u>1:
		r = 2-u
	else:
		r = u
			
	return array([r*cos(t), r*sin(t)])


class ps2gun:
	def __init__(self, name, empire, type, maxdmg, maxdmg_dist, mindmg, mindmg_dist, firemode, rlt_short, rlt_long, magsize, ammopool, vrec, hrec_min, hrec_max, hrec_tol, rangl_min, rangl_max, recdec, fsrm, cof_astst, cof_astmv,cof_acrst, cof_acrmv, cof_hstst, cof_hstmv, cof_hstsp, cof_hcrst, cof_hcrmv, blooma, bloomh,rof, bspeed, attachments):
		self.name = name
		self.empire = empire
		self.type = type
		self.maxdmg = maxdmg
		self.maxdmg_dist = maxdmg_dist
		self.mindmg = mindmg
		self.mindmg_dist = mindmg_dist
		self.firemode = firemode
		self.rlt_short = rlt_short
		self.rlt_long = rlt_long
		self.magsize = magsize
		self.ammopool = ammopool
		self.vrec = vrec
		self.hrec_min = hrec_min
		self.hrec_max = hrec_max
		self.hrec_tol = hrec_tol
		self.rangl_min = rangl_min
		self.rangl_max = rangl_max
		self.recdec = recdec
		self.fsrm = fsrm
		self.cof_astst = cof_astst
		self.cof_astmv = cof_astmv
		self.cof_acrst = cof_acrst
		self.cof_acrmv = cof_acrmv
		self.cof_hstst = cof_hstst
		self.cof_hstmv = cof_hstmv
		self.cof_hstsp = cof_hstsp
		self.cof_hcrst = cof_hcrst
		self.cof_hcrmv = cof_hcrmv
		self.blooma = blooma
		self.bloomh = bloomh
		self.rof = rof
		self.bspeed = bspeed

		self.attachments = []
		self.apply_attachments(attachments)

		self.cofdec = 20.
		self.cofinc = 50.
		self.tps = 60./self.rof
		
		self.time = 0.
		self.blocktime = 0.
		self.stance = 'hstst'
		self.cof_now = self.cof_hstst
		self.aimpoint = array([0., 0.])
		self.ret_disp = array([0., 0.])
		self.hrec_applied = 0.
	
	def apply_attachments(self, attachments):
		
		for attachment in attachments:
			if attachment == "Compensator":
				if self.name == "AC-X11":
					self.vrec *= 0.80
				elif self.name == "Reaper DMR" or self.name == "SABR-13":
					self.vrec *= 0.75
				else:
					self.vrec *= 0.85
				self.cof_hstst *= 1.2
				self.cof_hstmv *= 1.2
				self.cof_hstsp *= 1.2
				self.cof_hcrst *= 1.2
				self.cof_hcrmv *= 1.2
				
			elif attachment == "Suppressor":
				if self.type == "PISTOL":
					self.bspeed *= 0.88
				elif self.type == "SMG":
					self.bspeed *=0.8
				elif self.type == "CARBINE":
					self.bspeed *= 0.65
				elif self.name == "AF-8 RailJack":
					self.bspeed *= 0.5
				else:
					self.bspeed *= 0.6

				if self.type == "SMG" or self.type == "PISTOL":
					self.mindmg_dist -= 10
				else:
					self.mindmg_dist -= 20
				
				self.maxdmg_dist -= 5
			
			elif attachment == "Flash Suppressor":
				self.blooma *= 1.2
				self.bloomh *= 1.2
				
			elif attachment == "Forward Grip":
				self.hrec_min *= 0.75
				self.hrec_max *= 0.75
				self.hrec_tol -= 0.05

			elif attachment == "Advanced Forward Grip":
				self.hrec_min *= 0.67
				self.hrec_max *= 0.67
				self.hrec_tol -= 0.05

			elif attachment == "Laser Sight":
				self.cof_hstst *= 0.67
				self.cof_hstmv *= 0.67
				self.cof_hstsp *= 0.67
				self.cof_hcrst *= 0.67
				self.cof_hcrmv *= 0.67

			elif attachment == "Advanced Laser Sight":
				self.cof_hstst *= 0.6
				self.cof_hstmv *= 0.6
				self.cof_hstsp *= 0.6
				self.cof_hcrst *= 0.6
				self.cof_hcrmv *= 0.6
			
			elif attachment == "Soft Point Ammunition":
				self.bspeed *= 0.95
				self.maxdmg_dist += 5
			
			elif attachment == "High Velocity Ammunition":
				self.bspeed *= 1.05
				self.mindmg_dist += 10
				self.vrec *= 1.1
			else:
				print("Attachment " + attachment + " not implemented / nonexistent.")
				continue
			self.attachments.append(attachment)
			
	def statprint(self):
		print("Gun:		" + self.name + " ("+ self.empire + ")")
		print("Type:		" + self.type)
		print("Attachments: " + " ".join(self.attachments))
		print("Max. Damage:	" + str(self.maxdmg) + " @ " + str(self.maxdmg_dist))
		print("Min. Damage:	" + str(self.mindmg) + " @ " + str(self.mindmg_dist))
		print("Fire Mode:	" + self.firemode)
		print("Reload Time:	" + str(self.rlt_short) + " / " + str(self.rlt_long))
		print("Ammo Count:	" + str(self.magsize) + " / " + str(self.ammopool))
		print("Recoil Vert:	" + str(self.vrec))
		print("Recoil Horz:	" + str(self.hrec_min) + " - " + str(self.hrec_max) + " (" + str(self.hrec_tol)+ ")")
		print("Recoil Angl:	"+ str(self.rangl_min) + " - " + str(self.rangl_max))
		print("FSRM:		" + str(self.fsrm))
		print("Rc Decrease:	" + str(self.recdec))
		print("CoF ADS:	" + str(self.cof_acrst) + " / " + str(self.cof_acrmv) + "  |  " + str(self.cof_astst) + " / " + str(self.cof_astmv) )
		print("CoF Hip:	" + str(self.cof_hcrst) + " / " + str(self.cof_hcrmv) + "  |  " + str(self.cof_hstst) + " / " + str(self.cof_hstmv) + " / " + str(self.cof_hstsp) )
		print("Bloom:		" + str(self.blooma) + " / " + str(self.bloomh))
		print("RoF:		" + str(self.rof))
		print("Bullet Speed:	"+ str(self.bspeed))

	def startcof(self, stance):
		if stance == 'astst':
			return self.cof_astst
		if stance == 'astmv':
			return self.cof_astmv
		if stance == 'acrst':
			return self.cof_acrst
		if stance == 'acrmv':
			return self.cof_acrmv
		if stance == 'hstst':
			return self.cof_hstst
		if stance == 'hstmv':
			return self.cof_hstmv
		if stance == 'hstsp':
			return self.cof_hstsp
		if stance == 'hcrst':
			return self.cof_hcrst
		if stance == 'hcrmv':
			return self.cof_hcrmv

	def idle(self,duration):
		#process cof & ret cooldown since last update
		
		
		if duration > self.blocktime:
			timeleft = duration - self.blocktime
			self.blocktime = 0.
		
			targetcof = self.startcof(self.stance)
			if self.cof_now > targetcof:
				self.cof_now -= timeleft * self.cofdec
				if self.cof_now < targetcof:
					self.cof_now = targetcof
			elif self.cof_now < targetcof:
				self.cof_now += timeleft * self.cofinc
				if self.cof_now > targetcof:
					self.cof_now = targetcof
			
			retlen = norm(self.ret_disp)
			if retlen<=timeleft*self.recdec:
				self.ret_disp[:] = 0.
			else:
				self.ret_disp *= 1. - self.recdec*timeleft/retlen
		else:
			self.blocktime -= duration
		
		self.time += duration

	def set_stance(self, stance):
		self.stance = stance
	
	def set_aimpoint(self, aimpoint):
		self.aimpoint = aimpoint

	def ret_now(self):
		return self.aimpoint + self.ret_disp

	def damage(self,metersaway):
		if metersaway<=self.maxdmg_dist:
			return self.maxdmg
		elif metersaway>=self.mindmg_dist:
			return self.mindmg
		else:
			return self.maxdmg - (metersaway - self.maxdmg_dist)/(self.mindmg_dist-self.maxdmg_dist)*(self.maxdmg-self.mindmg)

	def trigger(self, duration, nocof, vrec_mode, hrec_mode):
		
		if duration > self.blocktime:
			
			timeleft = duration - self.blocktime
			nshots = int(timeleft//self.tps) + 1
			self.blocktime = self.tps - (nshots * self.tps - timeleft)
		
			self.hrec_applied = 0.
			
			shots = ndarray((nshots, 2))
			
			#print(nshots)
		
			randval = random_sample()
			randangl = pi/180. * ((self.rangl_max - self.rangl_min) * randval + self.rangl_min)
		
			#print("randangl: " + str(randangl * 180. / pi))
			
			for itshot in range(nshots):
				# SHOT
				shots[itshot] = self.ret_now().copy()
			
				# COF
				
				if not nocof:
					shots[itshot] += self.cof_now * rand_unicirc()
		
				# RECOIL
				
				recoil = array([0., 0.])
				
				if not vrec_mode=="fullcomp":
					recoil[1] += self.vrec
					if itshot == 0:
						recoil[1] *= self.fsrm
					
					if vrec_mode=="constcomp":
						recoil[1] -= self.vrec
				
				if not hrec_mode=="fullcomp":
					randval = random_sample()
					recoil[0] =  (self.hrec_max - self.hrec_min) * randval + self.hrec_min
				
					if self.hrec_applied >= self.hrec_tol-0.00001:
						randside = 0.
					elif self.hrec_applied <= - self.hrec_tol+0.00001:
						randside = 1.
					else:
						randside = random_sample()

					if randside < 0.5:
						recoil[0] *= -1.
			
				self.hrec_applied += recoil[0]
			
				#print("rec raw: " + str(recoil))
				#print("hrec applied sum: " + str(self.hrec_applied))
		
			
				recx = recoil[0] * cos(randangl) + recoil[1] * sin(randangl)
				recy = recoil[1] * cos(randangl) - recoil[0] * sin(randangl)
				recoil[0] = recx
				recoil[1] = recy
			
				self.ret_disp += recoil

				#print("rec final: " + str(recoil))
				#print("ret now: " + str(self.ret_now()))

				# BLOOM
			
				if self.stance[0] == 'h':
					self.cof_now += self.bloomh
				elif self.stance[0] == 'a':
					self.cof_now += self.blooma
	
				cofmax = 7. # not sure and not the same for all weapons
				if self.cof_now > cofmax:
					self.cof_now = cofmax
	
				#print("cof now: " + str(self.cof_now))
				
		else:
			self.blocktime -= duration

		self.time += duration
		return shots

class hitbox2D:
	def __init__(self, edgelengths, position):
		self.edgelengths = edgelengths
		self.position = position
		
		self.a = self.edgelengths[0]
		self.b = self.edgelengths[1]
	
		self.x = self.position[0]
		self.y = self.position[1]
		self.z = self.position[2]


class playerTarget2D:
	def __init__(self, position):
		self.position = position

		self.head = hitbox2D(array([0.25,0.25]),array([0.0,1.725,0.0]) + self.position)
		self.torso = hitbox2D(array([0.5,0.7]),array([0.0,1.25,0.0]) + self.position)
		self.legs = hitbox2D(array([0.5,0.9]),array([0.0,0.45,0.0]) + self.position)
	
	def hitboxes(self):
		return [self.head, self.torso, self.legs]
	
	def rect_collection(self, metersaway):
		rectArr = []
		pi180 = 180./pi
		for hitbox in self.hitboxes():
			recta = 2*arctan2(0.5*hitbox.a,metersaway)*pi180
			rectb = 2*arctan2(0.5*hitbox.b,metersaway)*pi180
			rectxy = array([arctan2(hitbox.x,metersaway),arctan2(hitbox.y,metersaway)])*pi180
			
			rectArr = append(rectArr,mpatches.Rectangle(array([-0.5*recta, -0.5*rectb])+rectxy, recta, rectb))
		return rectArr, PatchCollection(rectArr)

def burstseq(gun, burstlen, idlelen, numbursts, nocof, vrec_mode, hrec_mode):
	for itburst in range(numbursts):
		if itburst == 0:
			shots = gun.trigger(burstlen, nocof, vrec_mode, hrec_mode)
		else:
			shots = append(shots,gun.trigger(burstlen, nocof, vrec_mode, hrec_mode),axis = 0)
		gun.idle(idlelen)

	return shots

def rect_contains(rect,x,y):
	insideX = (rect.get_x()<=x and rect.get_x()+rect.get_width()>=x)
	insideY = (rect.get_y()<=y and rect.get_y()+rect.get_height()>=y)
	return (insideX and insideY)

with open('PS2 Weapon Data Sheets AUG06 - Gun Stuff.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	itr = 0
	for row in spamreader:
		#if itr == 1:
		#	print(row)
		#if itr > 1:
		if row[0] == "NC6A Godsaw":
			testgun = self = ps2gun(row[0], row[1], row[2], float(row[3].split('@')[0]), float(row[3].split('@')[1][:-1]),float(row[4].split('@')[0]), float(row[4].split('@')[1][:-1]), row[5], float(row[6]), float(row[7]), int(row[8]), int(row[9]), float(row[10]), float(row[11]), float(row[12]), float(row[13]), float(row[14]), float(row[15]), float(row[17]), float(row[18]), float(row[20]), float(row[21]), float(row[22]), float(row[23]), float(row[24]), float(row[25]), float(row[26]), float(row[27]), float(row[28]), float(row[29]), float(row[30]), float(row[31]), float(row[32]),[])
			# "Soft Point Ammunition" "High Velocity Ammunition" "Forward Grip" "Advanced Forward Grip" "Laser Sight" "Advanced Laser Sight" "Compensator"
			testgun.statprint()
			testgun.set_stance('hstst')
			
			metersaway = 10.
			nowdmg = testgun.damage(metersaway)
			print(nowdmg)
			
			nocof = False
			vrec_comp = "fullcomp"
			hrec_comp = "none"
			
			aimcof = 0.0
			
			target = playerTarget2D(array([0.0, -1.5, metersaway]))
			rectArr, collection = target.rect_collection(metersaway)
			
			bestnshots = 0
			allbestaimy = 0.
			allbestdps = 0.
			
			for nshots in range(1,10,1):
				print("Nshots: " + str(nshots))
				
				idlelen = max([self.tps, 0.25])
				burstlen = max([(nshots-1)*self.tps, 0.05])
				numbursts = 250/nshots
			
				bestaimy = 0.
				bestdps = 0.
				for aimy in arange(-75./metersaway,25./metersaway,2.5/metersaway):
					testgun.idle(1)
					testgun.set_aimpoint(array([0.0,aimy]))
				
					shots = burstseq(testgun, burstlen, idlelen, numbursts,nocof, vrec_comp, hrec_comp)
				
					totdmg = 0.
					for shot in shots:
						
						shot += aimcof * rand_unicirc()	# modeled inaccuracy because of player aim
						
						if rect_contains(rectArr[0], shot[0],shot[1]):
							totdmg += 2.*nowdmg
						elif rect_contains(rectArr[1], shot[0], shot[1]):
							totdmg += nowdmg
						elif rect_contains(rectArr[2], shot[0], shot[1]):
							totdmg += 0.9*nowdmg
				
					dps = totdmg/(burstlen + idlelen)/numbursts
					
					print(dps, aimy)
					if dps > bestdps:
						bestdps = dps
						bestaimy = aimy
				print(nshots, bestdps, bestaimy)
				if bestdps > allbestdps:
					allbestdps = bestdps
					allbestaimy = bestaimy
					bestnshots = nshots
		
			nshots = bestnshots
			burstlen = max([(nshots-1)*self.tps, 0.05])
			numbursts = 250/nshots
		
			print(bestnshots, allbestdps, allbestaimy)
			testgun.idle(1)
			testgun.set_aimpoint(array([0.0, allbestaimy]))
			
			shots = burstseq(testgun, burstlen, idlelen, numbursts,nocof, vrec_comp, hrec_comp)
			for shot in shots:
				shot += aimcof * rand_unicirc()
			
			#print(shots)
			
			plotrangeX = 20./metersaway
			plotrangeY = 40./metersaway
			binsize = 0.1
			drawhist = False
			
			fig = figure()
			ax = fig.add_subplot(111,aspect='equal')
			
			print(collection)
			ax.add_collection(collection)
			
			if drawhist:
				xedges = arange(-plotrangeX,plotrangeX + binsize,binsize)
				yedges = arange(-plotrangeY,plotrangeY + binsize,binsize)
				H, xedges, yedges = histogram2d(-shots[:,1],-shots[:,0], bins=(xedges, yedges))
				#imshow(H, interpolation='nearest')
				X, Y = meshgrid(xedges, yedges)
				ax.pcolormesh(X, Y, H)
				#set_aspect('equal')
			else:
				shotplot = ax.plot(shots[:,0],shots[:,1],'ro')
				xlim(-plotrangeX,plotrangeX)
				ylim(-plotrangeY*2,plotrangeY)
		
			show()
		
		
		
		
		itr += 1


#testgun = ps2gun()