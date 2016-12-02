from django.shortcuts import render
from django.http import HttpResponseRedirect
from photos.forms import ImageForm
from photos.models import Image

import numpy as np

import urllib 
import h5py 

import sys
import os

from scipy import misc


def image_upload(request):
    teste = []
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/signin/?next=%s' % request.path)
    else:
        if request.method == 'POST':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.user = request.user
                image.save()
                images = indexing_photos(request.FILES["image"], request.user.id)
                teste = images
                return render(request, 'image_upload.html', {'form': form, 'images': images})
        else:
            form = ImageForm()

        test = Image.objects.filter(user=request.user)
        images ={img.image.url for img in test}
        return render(request, 'image_upload.html', {'form': form, 'images': images})


labels = [] # Initialising labels as an empty array.

def indexing_photos(uploaded_image, user_id):

    images_path = 'media/user_{0}'.format(user_id)

    vectors, img_files = load_dataset_hist(images_path)
    KNN = NearestNeighbors(K=len(img_files), images_path=images_path)
    KNN.setXtr(vectors)

    # Freeing memory:
    del vectors
    KNN.setFilesList(img_files)

    images = KNN.retrieve(get_hist('{0}/{1}'.format(images_path, uploaded_image)))

    return images


def get_hist(filename):
    image =  misc.imread(filename)
    image = image[::4,::4,:]
    # Normalizing images:
    im_norm = (image-image.mean())/image.std()
    
    # Computing a 10-bin histogram in the range [-e, +e] (1 standard deviationto 255 for each of the colours:
    # (the first element [0] is the histogram, the second [1] is the array of bins.)
    hist_red = np.histogram(im_norm[:,:,0], range=(-np.e,+np.e))[0] 
    hist_green = np.histogram(im_norm[:,:,1], range=(-np.e,+np.e))[0]
    hist_blue = np.histogram(im_norm[:,:,2], range=(-np.e,+np.e))[0]
    # Concatenating them into a 30-dimensional vector:
    histogram = np.concatenate((hist_red, hist_green, hist_blue)).astype(np.float)
    return histogram/histogram.sum()

def load_dataset_hist(images_path):
    # Load/build a dataset of vectors (i.e. a big matrix) of RGB histograms.
    vectors_filename = os.path.join(images_path, 'vectors_hist.h5')

    # Build a list of JPG files (change if you want other image types):
    os.listdir(images_path)
    img_files = [f for f in os.listdir(images_path) if (('jpg' in f) or ('JPG') in f)]

    vectors = np.zeros((len(img_files), 30))
    for (f,n) in zip(img_files, range(len(img_files))):
        vectors[n] = get_hist(os.path.join(images_path, f))
                
    with h5py.File(vectors_filename, 'w') as f:
        f.create_dataset('vectors', data=vectors)
        f.create_dataset('img_files', data=img_files)

    return vectors, img_files


class NearestNeighbors:
    def __init__(self, K=None, Xtr=[], images_path='Photos/', img_files=[], labels=np.empty(0)):
        # Setting defaults
        self.K = K
        self.Xtr = Xtr
        self.images_path = images_path
        self.img_files = img_files
        self.labels = labels

    def setXtr(self, Xtr):
        """ X is N x D where each row is an example."""
        # the nearest neighbor classifier simply remembers all the training data
        self.Xtr = Xtr
        
    def setK(self, K):
        """ K is the number of samples to be retrieved for each Query."""
        self.K = K

    def setImagesPath(self,images_path):
        self.images_path = images_path
        
    def setFilesList(self,img_files):
        self.img_files = img_files

    def setLabels(self,labels):
        self.labels = labels
        
    def predict(self, x):
        """ x is a test (query) sample vector of 1 x D dimensions """
    
        # Compare x with the training (dataset) vectors
        # using the L1 distance (sum of absolute value differences)

        # p = 1.
        # distances = np.power(np.sum(np.power(np.abs(X-x),p), axis = 1), 1./p)
        distances = np.sum(np.abs(self.Xtr-x), axis = 1)
        # distances = 1-np.dot(X,x)
    
        # plt.figure(figsize=(15, 3))
        # plt.plot(distances)
        # print np.argsort(distances)
        return np.argsort(distances) # returns an array of indices of of the samples, sorted by how similar they are to x.

    def retrieve(self, x):

        nearest_neighbours = self.predict(x)
        images = []

        for n in range(self.K):
            idx = nearest_neighbours[n]
            image = (os.path.join(self.images_path, self.img_files[idx]))
            images.append('/' + image)

        return images