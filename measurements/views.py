
from django.shortcuts import render, redirect, get_object_or_404

from .models import Measurement
from .forms import MeasurementForm


def measurement_list(request):

    search = request.GET.get(
        'search',
        ''
    )

    measurements = Measurement.objects.all().order_by(
        '-created_at'
    )

    if search:

        measurements = measurements.filter(
            customer__name__icontains=search
        )

    return render(
        request,
        'measurements/measurement_list.html',
        {
            'measurements': measurements,
            'search': search
        }
    )


def add_measurement(request):

    if request.method == 'POST':

        form = MeasurementForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'measurement_list'
            )

    else:

        form = MeasurementForm()

    return render(
        request,
        'measurements/add_measurement.html',
        {
            'form': form
        }
    )


def view_measurement(request, id):

    measurement = get_object_or_404(
        Measurement,
        id=id
    )

    return render(
        request,
        'measurements/view_measurement.html',
        {
            'measurement': measurement
        }
    )


def edit_measurement(request, id):

    measurement = get_object_or_404(
        Measurement,
        id=id
    )

    if request.method == 'POST':

        form = MeasurementForm(
            request.POST,
            instance=measurement
        )

        if form.is_valid():

            form.save()

            return redirect(
                'measurement_list'
            )

    else:

        form = MeasurementForm(
            instance=measurement
        )

    return render(
        request,
        'measurements/edit_measurement.html',
        {
            'form': form,
            'measurement': measurement
        }
    )


def delete_measurement(request, id):

    measurement = get_object_or_404(
        Measurement,
        id=id
    )

    if request.method == 'POST':

        measurement.delete()

        return redirect(
            'measurement_list'
        )

    return render(
        request,
        'measurements/delete_measurement.html',
        {
            'measurement': measurement
        }
    )

