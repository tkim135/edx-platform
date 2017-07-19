$(function () {
    var designationsWithDependencies = [
        'MD',
        'MD,PhD',
        'DO',
        'MBBS'
    ];
    function updateRequirements(selector, shouldShow) {
        var element = $(selector);
        if (shouldShow) {
            element.find('LABEL').addClass('required');
            element.show();
        } else {
            element.find('LABEL').removeClass('required');
            element.hide();
        }
    }
    $('body').on('change', '#register-affiliation', function() {
        var affiliation = $(this).find(':selected').text();
        var isStanford = (affiliation === 'Stanford University');
        updateRequirements('.select-stanford_department', isStanford);
        updateRequirements('.text-sunet_id', isStanford);
        var $other = $('.text-other_affiliation');
        if (affiliation === 'Not affiliated with Stanford Medicine') {
            $other.show();
            $other.find('INPUT').attr('required', true);
            $other.find('INPUT').prev('LABEL').addClass('required');
        } else {
            $other.hide();
            $other.find('INPUT').attr('required', false);
            $other.find('INPUT').prev('LABEL').removeClass('required');
        }
    });
    $('body').on('change', '#register-specialty', function() {
        var select = $('#register-sub_specialty');
        var wrapper = $('.select-sub_specialty');
        var source = $(this).children("option:selected").val();
        // JQuery can't handle & in selectors
        source = source.replace('_&_', '_');
        source = source.replace('(', '\\(');
        var specialties = $('.specialty_' + source);
        if (specialties.length != 1) {
            wrapper.hide();
        } else {
            select.empty();
            select.append($(specialties.html()));
            wrapper.show();
        }
    });
    $('body').on('change', 'select#register-professional_designation', function() {
        var dependentRequiredFields = [
            '#register-license_number',
            '#register-license_country',
            '#register-physician_status',
            '#register-patient_population',
            '#register-specialty'
        ].join(', ');
        var designation = $(this).find(':selected').text();
        if (designationsWithDependencies.indexOf(designation) > -1) {
            $(dependentRequiredFields).attr('required', true);
            $(dependentRequiredFields).prev('LABEL').addClass('required');
        } else {
            $(dependentRequiredFields).attr('required', false);
            $(dependentRequiredFields).prev('LABEL').removeClass('required');
        }
    });
    function onChangeCountry(that, stateSelector) {
        var country = $(that).find(':selected').text();
        if (country === 'United States') {
            $(stateSelector).attr('required', true);
            $(stateSelector).prev('LABEL').addClass('required');
        } else {
            $(stateSelector).attr('required', false);
            $(stateSelector).prev('LABEL').removeClass('required');
        }
    }
    $('body').on('change', '#register-country', function() {
        onChangeCountry(this, '#register-state');
    });
    $('body').on('change', '#register-license_country', function() {
        onChangeCountry(this, '#register-license_state');
    });
});
