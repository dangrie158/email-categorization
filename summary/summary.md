## ~20000 samples:

### Categorization
mult_nb:        0.464458
mult_nb_tfidf:  0.346288
bern_nb:        370786
bern_nb_tfidf:  0.370786
svc:            0.455572
svc_tfidf:      0.480070
rf:             0.463710
rf_tfidf:       0.461219

                400 dimentional (9.37 GB)       200 dimensional (4.9GB)

argmax(LL):     0.645740707807                   0.658723101547
word2doc:       0.46478990201                    0.464457731274
CNN:            -                                0.2759 @ [3,4,5]       0.2602 @ [12]

### Clustering:
MiniBatchKMeans:
	homogenity:	  0.233553017635                   0.236841050147
	completeness:	0.226445794028                   0.249476009557
	v-measure:	  0.22994450066                    0.242994395985

AffinityPropagation:
	homogenity:	  0.791271760203                   0.652669953895
	completeness:	0.201767501168                   0.190574928079
	v-measure:	  0.321544035591                   0.295009272351

MeanShift:
	homogenity:	 -2.79616603853e-16               -2.79616603853e-16
	completeness:	1.0                              1.0
	v-measure:	 -5.59233207705e-16               -5.59233207705e-16

SpectralClustering:
	homogenity:	  0.00926710375476                 0.00789771144523
	completeness:	0.115924832081                   0.130907002339
	v-measure:	  0.017162246745                   0.0148966948232

Ward:
	homogenity:	  0.259648022342                   0.26562522413
	completeness:	0.268177584554                   0.268206528374
	v-measure:	  0.26384388539                    0.266909635398

AgglomerativeClustering:
	homogenity:	  0.0106941242306                  0.0106941242306
	completeness:	0.341135629001                   0.341135629001
	v-measure:	  0.0207381369114                  0.0207381369114

DBSCAN:
	homogenity:	  0.0451934853679                  0.0451934853679
	completeness:	0.159479197566                   0.159479197566
	v-measure:	  0.0704287516866                  0.0704287516866

Birch:
	homogenity:	  0.256166859527                   0.279111972684
	completeness:	0.248528220592                   0.266110719439
	v-measure:	  0.252289734062                   0.272456333634

~40000 samples:
