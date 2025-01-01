from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_mail import Mail, Message
from . import db, mail
from . import models
import base64
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/home', methods=['GET', 'POST'])
def home():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    else:
        if session['email'] == 'admin12@gmail.com':
            return redirect(url_for('views.admin'))
            
    information = models.Info.query.all()
    return render_template("home.html", information=information)

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        if 'email' not in session:
            return redirect(url_for('auth.login'))
        else:
            if session['email'] == 'admin12@gmail.com':
                return redirect(url_for('views.admin'))
            else:
                return redirect(url_for('views.home'))
    return render_template("contact.html")

@views.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    else:
        if not session['email'] == 'admin12@gmail.com':
            return redirect(url_for('views.home'))

    information = models.Info.query.all()
    return render_template("admin.html", information=information)

@views.route('/newseminar', methods=['GET', 'POST'])
def newseminar():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    elif not session['email'] == 'admin12@gmail.com':
        return redirect(url_for('views.home'))
    
    if request.method == "POST":
        name = request.form['name']
        negeri = request.form['negeri']
        daerah = request.form['daerah']
        desc = request.form['desc']
        rating = request.form.get('rating')
        price = request.form['price']
        location = request.form['location']
        capacity = request.form['pax']
        facility = request.form['facility']
        contact = request.form['contact']
        link = request.form['link']

        image = request.files.get('image')
        image2 = request.files.get('image2')
        image3 = request.files.get('image3')
        image4 = request.files.get('image4')

        image_data = image.read() if image else None
        image_data2 = image2.read() if image2 else None
        image_data3 = image3.read() if image3 else None
        image_data4 = image4.read() if image4 else None
        
        new_info = models.Seminar(
            link=link,
            name=name,
            negeri=negeri,
            daerah=daerah,
            desc=desc,
            rating=rating,
            image=image_data,
            image2=image_data2,
            image3=image_data3,
            image4=image_data4,
            price=price,
            location=location,
            capacity=capacity,
            facility=facility,
            contact=contact
        )
        db.session.add(new_info)
        db.session.commit()
        flash("Information added successfully!", category="success")

        return redirect(url_for('views.admin'))
    return render_template("newseminar.html")

@views.route('/addinfo', methods=['GET', 'POST'])
def addinfo():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    elif not session['email'] == 'admin12@gmail.com':
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        name = request.form.get('name')
        image1 = request.files.get('image1')
        image2 = request.files.get('image2')
        image3 = request.files.get('image3')

        if not name or not (image1 or image2 or image3):
            flash('Please provide a name and at least one image.', category='error')
            return redirect(url_for('views.admin'))

        image_data1 = image1.read() if image1 else None
        image_data2 = image2.read() if image2 else None
        image_data3 = image3.read() if image3 else None

        new_info = models.Info(
            name=name,
            image1=image_data1,
            image2=image_data2,
            image3=image_data3
        )
        db.session.add(new_info)
        db.session.commit()

        flash('Information added successfully!', category='success')
        return redirect(url_for('views.admin'))

    information = models.Info.query.all()
    return render_template("admin.html", info=True, information=information)

@views.route('/deleteInfo')
def deleteInfo():
    id = request.args.get('id')
    value = models.Info.query.filter_by(id=id).first()
    db.session.delete(value)
    db.session.commit()

    return redirect(url_for('views.admin'))

@views.route('/editInfo', methods=['GET', 'POST'])
def editInfo():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    elif not session['email'] == 'admin12@gmail.com':
        return redirect(url_for('views.home'))
    
    id = request.args.get('id')
    value = models.Info.query.filter_by(id=id).first()
    if request.method == "POST":
        name = request.form.get('name')
        image1 = request.files.get('image1')
        image2 = request.files.get('image2')
        image3 = request.files.get('image3')

        if name:
            value.name = name
        if image1:
            value.image1 = image1.read()
        if image2:
            value.image2 = image2.read()
        if image3:
            value.image3 = image3.read()

        db.session.commit()
        flash("Information edited successfully!", category="success")
        return redirect(url_for('views.admin'))

    return render_template('addinfo.html', value=value)

@views.route('/seminarAdmin', methods=['GET', 'POST'])
def seminarAdmin():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    elif not session['email'] == 'admin12@gmail.com':
        return redirect(url_for('views.home'))
    
    negeri = request.args.get('negeri')
    daerah = request.args.get('daerah')

    value = models.Seminar.query.filter_by(negeri=negeri, daerah=daerah).all()
    return render_template('seminarAdmin.html', value=value, negeri=negeri, daerah=daerah)

@views.route('/seminarRoom', methods=['GET', 'POST'])
def seminarRoom():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    elif session['email'] == 'admin12@gmail.com':
        return redirect(url_for('views.admin'))
    
    negeri = request.args.get('negeri')
    daerah = request.args.get('daerah')

    value = models.Seminar.query.filter_by(negeri=negeri, daerah=daerah).all()
    return render_template('seminarRoom.html', value=value, negeri=negeri, daerah=daerah)

@views.route('/deleteSeminar', methods=['GET', 'POST'])
def deleteSeminar():
    id = request.args.get('id')
    negeri = request.args.get('negeri')
    daerah = request.args.get('daerah')
    find_seminar = models.Seminar.query.filter_by(id=id).first()
    db.session.delete(find_seminar)
    db.session.commit()

    value = models.Seminar.query.filter_by(negeri=negeri, daerah=daerah).all()
    return redirect(url_for('views.seminarAdmin', value=value, negeri=negeri, daerah=daerah))

@views.route('/editSeminar', methods=['GET', 'POST'])
def editSeminar():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    elif not session['email'] == 'admin12@gmail.com':
        return redirect(url_for('views.home'))
    
    id = request.args.get('id')
    negeri = request.args.get('negeri')
    daerah = request.args.get('daerah')
    find_seminar = models.Seminar.query.filter_by(id=id).first()

    if request.method == "POST":
        name = request.form['name']
        negeri = request.form['negeri']
        daerah = request.form['daerah']
        desc = request.form['desc']
        rating = request.form.get('rating')
        price = request.form['price']
        location = request.form['location']
        link = request.form['link']
        capacity = request.form['pax']
        facility = request.form['facility']
        contact = request.form['contact']

        image = request.files.get('image')
        image2 = request.files.get('image2')
        image3 = request.files.get('image3')
        image4 = request.files.get('image4')
        find_seminar.name = name
        find_seminar.negeri = negeri
        find_seminar.daerah = daerah
        find_seminar.desc = desc
        find_seminar.rating = rating
        find_seminar.price = price
        find_seminar.location = location
        find_seminar.capacity = capacity
        find_seminar.facility = facility
        find_seminar.contact = contact
        find_seminar.link = link
        if image:
            find_seminar.image = image.read()
        if image2:
            find_seminar.image2 = image2.read()
        if image3:
            find_seminar.image3 = image3.read()
        if image4:
            find_seminar.image4 = image4.read()

        db.session.commit()
        flash("Seminar updated successfully!", category="success")
        return redirect(url_for('views.seminarAdmin', negeri=negeri, daerah=daerah))

    return render_template('editseminar.html', value=find_seminar)


@views.route('/gallery')
def gallery():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    elif not session['email'] == 'admin12@gmail.com':
        return render_template('gallery.html')
    else:
        return render_template('galleryAdmin.html')
    
@views.route('/viewDetail', methods=['GET', 'POST'])
def viewDetail():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    
    id = request.args.get('id')
    negeri = request.args.get('negeri')
    daerah = request.args.get('daerah')

    if request.method == 'POST':
        if session.get('email') == 'admin12@gmail.com':
            return redirect(url_for('views.seminarAdmin', negeri=negeri, daerah=daerah))
        elif not session.get('email') == 'admin12@gmail.com':
            return redirect(url_for('views.seminarRoom', negeri=negeri, daerah=daerah))
        else: 
            return redirect(url_for('auth.login'))
    
    # Fetch seminar details
    seminar = models.Seminar.query.filter_by(id=id, negeri=negeri, daerah=daerah).first()
    
    # Render the viewDetail template
    return render_template('viewDetail.html', value=seminar)


